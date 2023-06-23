"""Print a tree of objects in the Vantage system."""

import argparse
import asyncio
import contextlib
import logging
from typing import Optional

from aiovantage import Vantage
from aiovantage.config_client.objects import Area, Load


# Some ANSI escape codes for pretty printing
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"


def colorize(text: str, color: str) -> str:
    """Return text wrapped in the given ANSI color code."""
    return f"{color}{text}{RESET}"


def print_indented(text: str, indent_level: int) -> None:
    """Print text indented by the given number of levels."""
    indent = indent_level * "    "
    print(f"{indent}{text}")


def load_state(load: Load) -> str:
    """Return a string describing the state of a load."""
    if not load.level:
        return colorize("(OFF)", RED)
    elif load.level == 100:
        return colorize("(ON)", GREEN)
    else:
        return colorize(f"({load.level}%)", GREEN)


def print_area(vantage: Vantage, area: Optional[Area], indent: int = 0) -> None:
    """Recursively print an area and all its children."""
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


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="aiovantage example")
    parser.add_argument("host", help="hostname of Vantage controller")
    parser.add_argument("--username", help="username for Vantage controller")
    parser.add_argument("--password", help="password for Vantage controller")
    parser.add_argument(
        "--debug", help="enable debug level logging", action="store_true"
    )
    parser.add_argument("--log", help="write debug log to file")
    return parser.parse_args()


def configure_logging(log_args: argparse.Namespace) -> None:
    """Configure debug logging."""
    logging.basicConfig(
        level=logging.DEBUG if log_args.debug else logging.INFO,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )
    if log_args.log:
        logging.getLogger().addHandler(logging.FileHandler(filename=args.log, mode='w'))


# Parse command line args and configure logging
args = parse_arguments()
configure_logging(args)


async def main() -> None:
    """Run code example."""

    # Connect to the Vantage controller
    async with Vantage(args.host, args.username, args.password) as vantage:
        # Preload all the objects we want to dump
        await vantage.initialize()

        # Recursively print the root area and all its children
        print_area(vantage, vantage.areas.get(area_id=0))


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)
