"""Fetch all loads from the Vantage controller, and print out any state changes."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage import Vantage
from aiovantage.events import ObjectAddedEvent, ObjectUpdatedEvent, VantageEvent
from aiovantage.objects import Load

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


def callback(event: VantageEvent[Load]) -> None:
    """Print out any state changes."""
    if isinstance(event, ObjectAddedEvent):
        print(f"[Load added] '{event.obj.name}' ({event.obj.id})")

    elif isinstance(event, ObjectUpdatedEvent):
        print(f"[Load updated] '{event.obj.name}' ({event.obj.id})")
        for attr in event.attrs_changed:
            print(f"    {attr} = {getattr(event.obj, attr)}")


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Connect to the Vantage controller
    async with Vantage(args.host, args.username, args.password) as vantage:
        # Subscribe to updates for all loads
        vantage.loads.subscribe(callback, ObjectAddedEvent, ObjectUpdatedEvent)

        # Fetch all known loads from the controller
        await vantage.loads.initialize()

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
