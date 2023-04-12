#!/usr/bin/env python3

import asyncio
import logging

from aiovantage import Vantage

logging.basicConfig(level=logging.DEBUG)


async def main() -> None:
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        await vantage.loads.initialize()
        await vantage.areas.initialize()

        for load in vantage.loads:
            print(f"{load.name}")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
