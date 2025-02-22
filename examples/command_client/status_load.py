"""Use a CommandClient to subscribe to status updates for LOAD objects."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage.command_client import EventStream
from aiovantage.events import Connected, Disconnected, Reconnected, StatusReceived

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


def on_connected(event: Connected) -> None:
    """Print out a message when connected."""
    print("Connected and monitoring for status updates...")


def on_disconnected(event: Disconnected) -> None:
    """Print out a message when disconnected."""
    print("Disconnected")


def on_reconnected(event: Reconnected) -> None:
    """Print out a message when reconnected."""
    print("Reconnected")


def on_status_received(event: StatusReceived) -> None:
    """Print out the status update for each event."""
    print(f"[{event.category}] id: {event.vid}, args: {event.args}")


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
        events.subscribe(Disconnected, on_disconnected)
        events.subscribe(Reconnected, on_reconnected)

        # Subscribe to status updates for LOAD objects (STATUS LOAD)
        events.subscribe_status(on_status_received, "LOAD")

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
