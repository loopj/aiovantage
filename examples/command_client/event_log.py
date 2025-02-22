"""Example of using the CommandClient to subscribe to system log events."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage.command_client import EventStream
from aiovantage.events import Connected, EnhancedLogReceived

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
parser.add_argument("--ssl", action=argparse.BooleanOptionalAction, default=True)
args = parser.parse_args()


def on_connected(event: Connected) -> None:
    """Print out the connection event."""
    print("Connected and monitoring for log events...")


def command_client_callback(event: EnhancedLogReceived) -> None:
    """Print out the log message for each event."""
    print(event.log)


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Create an EventStream client
    async with EventStream(
        args.host, args.username, args.password, ssl=args.ssl
    ) as events:
        # Subscribe to connection events
        events.subscribe(Connected, on_connected)

        # Subscribe to system log events
        events.subscribe_enhanced_log(command_client_callback, "SYSTEM")

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
