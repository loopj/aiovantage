import asyncio
import logging
from typing import Any

from aiovantage import HCClient

logging.basicConfig(level=logging.INFO)


def status_callback(status_type: str, object_id: int, args: Any) -> None:
    print(f"[{status_type}] object id: {object_id}, args: {args}")


async def main() -> None:
    client = HCClient("10.2.0.103", "administrator", "ZZuUw76CnL")
    await client.connect()
    await client.subscribe(status_callback)

    await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
