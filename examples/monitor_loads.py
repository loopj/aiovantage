#!/usr/bin/env python3

from os.path import abspath, dirname
from sys import path

path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio
import logging

from aiovantage import Vantage

logging.basicConfig(level=logging.INFO)


def event_callback(obj, args) -> None:
    print(f"Load updated: {obj} {args}")

async def main():
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        vantage.loads.subscribe(event_callback)
        await asyncio.sleep(3600)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass