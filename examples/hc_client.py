#!/usr/bin/env python3

from os.path import abspath, dirname
from sys import path

path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio
import logging
from typing import Any

from aiovantage.clients.hc import HCClient

logging.basicConfig(level=logging.INFO)


def event_callback(status_type: str, vid: int, args: Any) -> None:
    print(f"{status_type} vid: {vid}, args: {args}")


async def main() -> None:
    client = HCClient("10.2.0.103", "administrator", "ZZuUw76CnL")
    await client.initialize()
    await client.subscribe(event_callback, "LOAD", "BTN")
    await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
