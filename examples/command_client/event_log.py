"""Example of using the CommandClient to subscribe to system log events."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage.command_client import Event, EventStream, EventType

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


def command_client_callback(event: Event) -> None:
    """Print out the log message for each event."""
    if event["type"] == EventType.ENHANCED_LOG:
        print(event["log"])
    elif event["type"] == EventType.CONNECTED:
        print("Connected and monitoring for log events...")


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Create an EventStream client
    async with EventStream(args.host, args.username, args.password) as events:
        # Subscribe to connection events
        events.subscribe(command_client_callback, EventType.CONNECTED)

        # Subscribe to system log events
        events.subscribe_enhanced_log(command_client_callback, "SYSTEM")

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
