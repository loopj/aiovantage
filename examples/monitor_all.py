"""Fetch all objects from the Vantage controller, and print out any state changes."""

import argparse
import asyncio
import contextlib
import logging
from typing import Any

from aiovantage import Vantage, VantageEvent
from aiovantage.objects import SystemObject

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


def callback(event: VantageEvent, obj: SystemObject, data: dict[str, Any]) -> None:
    """Print out any state changes."""
    object_type = type(obj).__name__

    if event == VantageEvent.OBJECT_ADDED:
        print(f"[{object_type} added] '{obj.name}' ({obj.vid})")
    elif event == VantageEvent.OBJECT_UPDATED:
        print(f"[{object_type} updated] '{obj.name}' ({obj.vid})")
        for attr in data.get("attrs_changed", []):
            print(f"    {attr} = {getattr(obj, attr)}")


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Connect to the Vantage controller
    async with Vantage(args.host, args.username, args.password) as vantage:
        # Subscribe to updates for all objects
        vantage.subscribe(callback)

        # Fetch all known objects from the controller
        await vantage.initialize()

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
