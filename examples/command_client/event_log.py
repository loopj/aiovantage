import argparse
import asyncio
import logging

from aiovantage.command_client import CommandClient, Event, EventType

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--no-ssl", help="use non-ssl connection", action="store_true")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()

# Define callback function for Host Command events
def command_client_callback(event: Event) -> None:
    if event["tag"] == EventType.EVENT_LOG:
        print(event["log"])
    elif event["tag"] == EventType.CONNECTED:
        print("Connected and monitoring for log events...")


async def main() -> None:
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Create a Host Command client
    client = CommandClient(
        args.host, args.username, args.password, use_ssl=not args.no_ssl
    )

    # Subscribe to connection events
    client.subscribe(command_client_callback, EventType.CONNECTED)

    # Connect the client
    await client.connect()

    # Subscribe to system log events
    await client.subscribe_event_log(command_client_callback, "SYSTEM")

    # Keep running for a while
    await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
