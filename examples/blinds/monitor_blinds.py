"""Fetch all blinds from the Vantage controller, and print out any state changes."""

import asyncio
import contextlib
from typing import Any, Dict

from aiovantage import Vantage, VantageEvent
from aiovantage.config_client.objects import SystemObject

from debug_logging import configure_logging, parse_arguments

# Grab connection info from command line arguments
args = parse_arguments()


def callback(event: VantageEvent, obj: SystemObject, data: Dict[str, Any]) -> None:
    """Print out any state changes."""
    if event == VantageEvent.OBJECT_ADDED:
        print(f"[Blind added] '{obj.name}' ({obj.id})")

    elif event == VantageEvent.OBJECT_UPDATED:
        print(f"[Blind updated] '{obj.name}' ({obj.id})")
        for attr in data.get("attrs_changed", []):
            print(f"    {attr} = {getattr(obj, attr)}")


async def main() -> None:
    """Run code example."""
    configure_logging(args.debug)

    async with Vantage(args.host, args.username, args.password) as vantage:
        # Subscribe to updates for all loads
        vantage.blinds.subscribe(callback)

        # Fetch all known loads from the controller
        await vantage.blinds.initialize()

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)
