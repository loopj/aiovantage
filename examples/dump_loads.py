#!/usr/bin/env python3

from os.path import abspath, dirname
from sys import path
path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio
from aiovantage import Vantage

async def main():
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        for load in vantage.loads:
            print(f"{load.name} ({load.area.name})")

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass