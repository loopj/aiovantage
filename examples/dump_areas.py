import asyncio
import os

from aiovantage import Vantage
from aiovantage.aci_client.system_objects import Area

# Set your Vantage host ip, username, and password as environment variables
VANTAGE_HOST = os.getenv("VANTAGE_HOST", "vantage.local")
VANTAGE_USER = os.getenv("VANTAGE_USER")
VANTAGE_PASS = os.getenv("VANTAGE_PASS")

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
    async with Vantage(VANTAGE_HOST, VANTAGE_USER, VANTAGE_PASS) as vantage:
        await vantage.initialize()

        root = vantage.areas.root
        if root is not None:
            for area in vantage.areas.filter(area_id=root.id):
                print_area(vantage, area)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
