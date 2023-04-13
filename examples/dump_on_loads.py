#!/usr/bin/env python3

import asyncio
import logging

from aiovantage import Vantage

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        await vantage.loads.initialize()

        for load in vantage.loads.on():
            print(f"{load.name}")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
