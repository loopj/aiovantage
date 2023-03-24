#!/usr/bin/env python3

from os.path import abspath, dirname
from sys import path
path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio
from aiovantage import Vantage

async def main():
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        for area in vantage.areas:
            print(f"{area.name}:")

            if area.parent:
                print("    Parent:")
                print(f"        {area.parent.name}")

            if area.areas:
                print("    Areas:")
                for area in area.areas:
                    print(f"        {area.name}")

            if area.stations:
                print("    Stations:")
                for station in area.stations:
                    print(f"        {station.name}")

            if area.loads:
                print("    Loads:")
                for load in area.loads:
                    print(f"        {load.name}")

            if area.dry_contacts:
                print("    Dry Contacts:")
                for dry_contact in area.dry_contacts:
                    print(f"        {dry_contact.name}")
            
            print()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass