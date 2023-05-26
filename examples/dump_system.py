import argparse
import asyncio
import logging
from typing import Optional

from aiovantage import Vantage
from aiovantage.config_client.objects import Area, Load


# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


# Some ANSI escape codes for pretty printing
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"


def colorize(text: str, color: str) -> str:
    return f"{color}{text}{RESET}"


def print_indented(text: str, indent_level: int) -> None:
    indent = indent_level * "    "
    print(f"{indent}{text}")


def load_state(load: Load) -> str:
    if not load.level:
        return colorize("(OFF)", RED)
    elif load.level == 100:
        return colorize("(ON)", GREEN)
    else:
        return colorize(f"({load.level}%)", GREEN)


def print_area(vantage: Vantage, area: Optional[Area], indent: int = 0) -> None:
    if area is None:
        return

    # Print the area name
    print_indented(colorize(area.name, CYAN), indent)

    # Print loads in this area, if any
    loads = vantage.loads.filter(area_id=area.id)
    if loads:
        print_indented(colorize("Loads", YELLOW), indent + 1)
        for load in loads:
            print_indented(f"- {load.name} {load_state(load)}", indent + 1)
        print()

    # Print RGB loads in this area, if any
    rgb_loads = vantage.rgb_loads.filter(area_id=area.id)
    if rgb_loads:
        print_indented(colorize("RGB Loads", YELLOW), indent + 1)
        for rgb_load in rgb_loads:
            print_indented(f"- {rgb_load.name} ", indent + 1)
        print()

    # Print stations in this area, if any
    stations = vantage.stations.filter(area_id=area.id)
    if stations:
        print_indented(colorize("Stations", YELLOW), indent + 1)
        for station in stations:
            print_indented(f"- {station.name}", indent + 1)
        print()

    # Print dry contacts in this area, if any
    dry_contacts = vantage.dry_contacts.filter(area_id=area.id)
    if dry_contacts:
        print_indented(colorize("Dry Contacts", YELLOW), indent + 1)
        for dry_contact in dry_contacts:
            print_indented(f"- {dry_contact.name}", indent + 1)
        print()

    # Print any child areas
    child_areas = vantage.areas.filter(area_id=area.id)
    if child_areas:
        for child_area in child_areas:
            print_area(vantage, child_area, indent + 1)


async def main() -> None:
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Connect to the Vantage controller
    async with Vantage(args.host, args.username, args.password) as vantage:
        # Preload all the objects we want to dump
        await vantage.initialize()

        # Recursively print the root area and all its children
        print_area(vantage, vantage.areas.root)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
