"""Fetch all RGB loads from the Vantage controller, and print out any state changes."""

import argparse
import asyncio
import contextlib
import logging
from typing import Any, Dict

from aiovantage import Vantage, VantageEvent
from aiovantage.models import RGBLoadBase

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


def callback(event: VantageEvent, obj: RGBLoadBase, data: Dict[str, Any]) -> None:
    """Print out any state changes."""
    if event == VantageEvent.OBJECT_ADDED:
        print(f"[RGBLoad added] '{obj.name}' ({obj.id})")
    elif event == VantageEvent.OBJECT_UPDATED:
        print(f"[RGBLoad updated] '{obj.name}' ({obj.id})")
        for attr in data.get("attrs_changed", []):
            print(f"    {attr} = {getattr(obj, attr)}")


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Connect to the Vantage controller
    async with Vantage(args.host, args.username, args.password) as vantage:
        # Subscribe to RGB load updates
        vantage.rgb_loads.subscribe(callback)

        # Fetch all known RGB loads from the controller
        await vantage.rgb_loads.initialize()

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
