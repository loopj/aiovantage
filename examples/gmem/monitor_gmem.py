"""Fetch all variables from the Vantage controller, and print out any state changes."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage import Vantage
from aiovantage.events import ObjectAddedEvent, ObjectUpdatedEvent, VantageEvent
from aiovantage.objects import GMem

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


def callback(event: VantageEvent[GMem]) -> None:
    """Print out any state changes."""
    if isinstance(event, ObjectAddedEvent):
        print(f"[GMem added] '{event.obj.name}' ({event.obj.id})")

    elif isinstance(event, ObjectUpdatedEvent):
        print(f"[GMem updated] '{event.obj.name}' ({event.obj.id})")
        for attr in event.attrs_changed:
            print(f"    {attr} = {getattr(event.obj, attr)}")


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Connect to the Vantage controller
    async with Vantage(args.host, args.username, args.password) as vantage:
        # Subscribe to updates for all variables
        vantage.gmem.subscribe(callback)

        # Fetch all known variables from the controller
        await vantage.gmem.initialize()

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
