import asyncio
import os

from aiovantage.command_client import HCClient
from aiovantage.command_client.events import Event, EventType

# Set your Vantage host ip, username, and password as environment variables
VANTAGE_HOST = os.getenv("VANTAGE_HOST", "vantage.local")
VANTAGE_USER = os.getenv("VANTAGE_USER")
VANTAGE_PASS = os.getenv("VANTAGE_PASS")


def command_client_callback(event: Event) -> None:
    if event["tag"] == EventType.EVENT_LOG:
        print(event["log"])


async def main() -> None:
    # Connect to the Host Command client
    client = HCClient(VANTAGE_HOST, VANTAGE_USER, VANTAGE_PASS)
    await client.connect()

    # Subscribe to system log events
    await client.subscribe_event_log(command_client_callback, "SYSTEM")

    print("Connected and monitoring for log events...")
    await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
