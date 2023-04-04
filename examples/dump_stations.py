# !/usr/bin/env python3

from os.path import abspath, dirname
from sys import path

path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio
import logging

from aiovantage import Vantage

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        await vantage.initialize()

        for station in vantage.stations:
            print(f"{station.name}")

            if station.buttons:
                print("    Buttons:")
                for button in station.buttons:
                    print(f"        {button.name}")

            if station.dry_contacts:
                print("    Dry Contacts:")
                for dry_contact in station.dry_contacts:
                    print(f"        {dry_contact.name}")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
