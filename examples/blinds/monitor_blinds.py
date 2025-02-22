"""Fetch all blinds from the Vantage controller, and print out any state changes."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage import Vantage
from aiovantage.controllers import BlindTypes
from aiovantage.events import ObjectUpdated

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
parser.add_argument("--ssl", action=argparse.BooleanOptionalAction, default=True)
args = parser.parse_args()


def on_object_updated(event: ObjectUpdated[BlindTypes]) -> None:
    """Print out any state changes."""
    print(f"[Blind updated] '{event.obj.name}' ({event.obj.id})")
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
        # Fetch all known blinds from the controller
        await vantage.blinds.initialize()

        # Subscribe to updates for all blinds
        vantage.blinds.subscribe(ObjectUpdated, on_object_updated)

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
