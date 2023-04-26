import asyncio
import os
from typing import List

from aiovantage import HCClient

# Set your Vantage host ip, username, and password as environment variables
VANTAGE_HOST = os.getenv("VANTAGE_HOST", "vantage.local")
VANTAGE_USER = os.getenv("VANTAGE_USER")
VANTAGE_PASS = os.getenv("VANTAGE_PASS")


def status_callback(object_id: int, status_type: str, args: List[str]) -> None:
    print(f"[{status_type}] object id: {object_id}, args: {args}")


async def main() -> None:
    # Connect to the Host Command client
    client = HCClient(VANTAGE_HOST, VANTAGE_USER, VANTAGE_PASS)
    await client.connect()

    # Subscribe to status updates for LOAD objects (STATUS LOAD)
    await client.subscribe_status(status_callback, "LOAD")

    print("Connected and monitoring for status updates...")
    await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
