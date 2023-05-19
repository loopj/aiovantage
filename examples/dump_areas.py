import argparse
import asyncio
import logging

from aiovantage import Vantage
from aiovantage.config_client.objects import Area

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--no-ssl", help="use non-ssl connection", action="store_true")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()

# Some ANSI escape codes for pretty printing
RESET = "\033[0m"
YELLOW = "\033[33m"
CYAN = "\033[36m"


def print_indented(text: str, indent_level: int) -> None:
    indent = indent_level * "    "
    print(indent + text)


def print_area(vantage: Vantage, area: Area, level: int = 0) -> None:
    print_indented(f"{CYAN}{area.name}{RESET}", level)

    child_areas = list(vantage.areas.filter(area_id=area.id))
    if child_areas:
        for child_area in child_areas:
            print_area(vantage, child_area, level=level + 1)

    stations = list(vantage.stations.filter(area_id=area.id))
    if stations:
        print_indented(f"{YELLOW}Stations{RESET}", level + 1)
        for station in stations:
            print_indented(f"- {station.name}", level + 1)
        print()

    loads = list(vantage.loads.filter(area_id=area.id))
    if loads:
        print_indented(f"{YELLOW}Loads{RESET}", level + 1)
        for load in loads:
            print_indented(f"- {load.name}", level + 1)
        print()

    dry_contacts = list(vantage.dry_contacts.filter(area_id=area.id))
    if dry_contacts:
        print_indented(f"{YELLOW}Dry Contacts{RESET}", level + 1)
        for dry_contact in dry_contacts:
            print_indented(f"- {dry_contact.name}", level + 1)
        print()


async def main() -> None:
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    async with Vantage(
        args.host, args.username, args.password, use_ssl=not args.no_ssl
    ) as vantage:
        await vantage.initialize()

        root = vantage.areas.root
        if root is not None:
            for area in vantage.areas.filter(area_id=root.id):
                print_area(vantage, area)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
