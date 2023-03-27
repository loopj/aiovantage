#!/usr/bin/env python3

from os.path import abspath, dirname
from sys import path

path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio

from aiovantage import Vantage
from aiovantage.models import Area


def print_indented(text, indent_level):
    indent = indent_level * "    "
    print(indent + text)

def print_area(area: Area, level=0):
    print_indented(f"{area.name}", level)

    if area.areas:
        for obj in area.areas:
            print_area(obj, level=level+1)

    if area.stations:
        print_indented("Stations:", level+1)
        for obj in area.stations:
            print_indented(f"{obj.name}", level+2)

    if area.loads:
        print_indented("Loads:", level+1)
        for obj in area.loads:
            print_indented(f"{obj.name}", level+2)

    if area.dry_contacts:
        print_indented("Dry Contacts:", level+1)
        for obj in area.dry_contacts:
            print_indented(f"{obj.name}", level+2)

async def main():
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        root = next(iter(vantage.areas.filter(lambda a: a.parent_id == 0)))
        print_area(root)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass