"""Use a CommandClient to subscribe to status updates for LOAD objects."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage.command_client import (
    ConnectEvent,
    DisconnectEvent,
    Event,
    EventStream,
    ReconnectEvent,
    StatusEvent,
)

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


def command_client_callback(event: Event) -> None:
    """Print out the status update for each event."""
    if isinstance(event, StatusEvent):
        print(f"[{event.category}] id: {event.vid}, args: {event.args}")
    elif isinstance(event, ConnectEvent):
        print("Connected and monitoring for status updates...")
    elif isinstance(event, DisconnectEvent):
        print("Disconnected")
    elif isinstance(event, ReconnectEvent):
        print("Reconnected")


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Create an EventStream client
    async with EventStream(args.host, args.username, args.password) as events:
        # Subscribe to connection events
        events.subscribe(
            command_client_callback,
            ConnectEvent,
            DisconnectEvent,
            ReconnectEvent,
        )

        # Subscribe to status updates for LOAD objects (STATUS LOAD)
        events.subscribe_status(command_client_callback, "LOAD")

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
