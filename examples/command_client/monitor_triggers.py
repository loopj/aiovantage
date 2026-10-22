"""Example of monitoring which objects trigger which tasks, as they happen."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage.command_client import EventStream
from aiovantage.events import Connected, TriggerReceived

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
    print("Connected and monitoring for triggers...")


def on_trigger(event: TriggerReceived) -> None:
    """Print out the object that triggered each task."""
    trigger_type = event.trigger_type
    trigger = trigger_type.name if trigger_type is not None else str(event.event)

    print(f"{trigger}: {event.source} started task {event.destination}")


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

        # Subscribe to triggers
        events.subscribe_triggers(on_trigger)

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
