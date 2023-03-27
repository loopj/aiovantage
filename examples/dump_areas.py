#!/usr/bin/env python3

from os.path import abspath, dirname
from sys import path

path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio

from aiovantage import Vantage
from aiovantage.models.area import Area


def print_indented(text: str, indent_level: int) -> None:
    indent = indent_level * "    "
    print(indent + text)

def print_area(area: Area, level: int=0) -> None:
    print_indented(f"{area.name}", level)

    if area.areas:
        for child_area in area.areas:
            print_area(child_area, level=level+1)

    if area.stations:
        print_indented("Stations:", level+1)
        for station in area.stations:
            print_indented(f"{station.name}", level+2)

    if area.loads:
        print_indented("Loads:", level+1)
        for load in area.loads:
            print_indented(f"{load.name}", level+2)

    if area.dry_contacts:
        print_indented("Dry Contacts:", level+1)
        for dry_contact in area.dry_contacts:
            print_indented(f"{dry_contact.name}", level+2)

async def main() -> None:
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        root = next(iter(vantage.areas.filter(lambda a: a.parent_id == 0)))
        print_area(root)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass