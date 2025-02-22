"""Fetch all objects from the Vantage controller, and print out any state changes."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage import Vantage
from aiovantage.events import ObjectUpdated
from aiovantage.objects import SystemObject

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
parser.add_argument("--ssl", action=argparse.BooleanOptionalAction, default=True)
args = parser.parse_args()


def callback(event: ObjectUpdated[SystemObject]) -> None:
    """Print out any state changes."""
    print(f"[{type(event.obj).__name__} updated] '{event.obj.name}' ({event.obj.id})")
    for attr in event.attrs_changed:
        print(f"    {attr} = {getattr(event.obj, attr)}")


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Connect to the Vantage controller
    async with Vantage(
        args.host, args.username, args.password, ssl=args.ssl
    ) as vantage:
        # Fetch all known objects from the controller
        await vantage.initialize()

        # Subscribe to updates for all objects
        vantage.subscribe(ObjectUpdated, callback)

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
