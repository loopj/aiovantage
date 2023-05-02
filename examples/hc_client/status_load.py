import asyncio
import os

from aiovantage.command_client import HCClient
from aiovantage.command_client.events import Event, EventType

# Set your Vantage host ip, username, and password as environment variables
VANTAGE_HOST = os.getenv("VANTAGE_HOST", "vantage.local")
VANTAGE_USER = os.getenv("VANTAGE_USER")
VANTAGE_PASS = os.getenv("VANTAGE_PASS")


def command_client_callback(event: Event) -> None:
    if event["tag"] == EventType.STATUS:
        print(f"[{event['status_type']}] id: {event['id']}, args: {event['args']}")


async def main() -> None:
    # Connect to the Host Command client
    client = HCClient(VANTAGE_HOST, VANTAGE_USER, VANTAGE_PASS)
    await client.connect()

    # Subscribe to status updates for LOAD objects (STATUS LOAD)
    await client.subscribe_status(command_client_callback, "LOAD")

    print("Connected and monitoring for status updates...")
    await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
