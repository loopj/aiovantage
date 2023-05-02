import asyncio
import logging
from typing import List

from aiovantage import HCClient

logging.basicConfig(level=logging.DEBUG)

def status_callback(object_id: int, status_type: str, args: List[str]) -> None:
    print(f"[{status_type}] object id: {object_id}, args: {args}")


async def main() -> None:
    # Connect to the Host Command client
    client = HCClient("localhost", use_ssl=False, conn_timeout=1, read_timeout=5)
    await client.connect()

    # Subscribe to status updates for LOAD objects (STATUS LOAD)
    await client.subscribe_status(status_callback, "LOAD")

    print("Connected and monitoring for status updates...")
    await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
