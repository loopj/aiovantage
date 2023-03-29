#!/usr/bin/env python3

from os.path import abspath, dirname
from sys import path

path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio
import logging

from aiovantage import Vantage

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        await vantage.fetch_objects()

        for load in vantage.loads:
            print(f"{load.name} ({load.area.name if load.area else 'Unknown Area'})")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
