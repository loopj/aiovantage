import argparse
import asyncio
import logging

from aiovantage.command_client import HostCommandClient, Event, EventType

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--no-ssl", help="use non-ssl connection", action="store_true")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


# Define callback function for command client events
def command_client_callback(event: Event) -> None:
    if event["tag"] == EventType.STATUS:
        print(f"[{event['status_type']}] id: {event['id']}, args: {event['args']}")
    elif event["tag"] == EventType.CONNECTED:
        print("Connected and monitoring for status updates...")
    elif event["tag"] == EventType.DISCONNECTED:
        print("Disconnected")
    elif event["tag"] == EventType.RECONNECTED:
        print("Reconnected")


async def main() -> None:
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Create a Host Command client
    async with HostCommandClient(
        args.host, args.username, args.password, ssl=not args.no_ssl
    ) as client:
        # Subscribe to connection events
        client.subscribe(
            command_client_callback,
            (EventType.CONNECTED, EventType.DISCONNECTED, EventType.RECONNECTED),
        )

        # Subscribe to status updates for LOAD objects (STATUS LOAD)
        await client.subscribe_status(command_client_callback, "LOAD")

        # Keep running for a while
        await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
