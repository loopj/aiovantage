"""Fetch all temperature sensors from the Vantage controller, and print any state changes."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage import Vantage
from aiovantage.events import ObjectAddedEvent, ObjectUpdatedEvent, VantageEvent
from aiovantage.objects import Temperature

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


def callback(event: VantageEvent[Temperature]) -> None:
    """Print out any state changes."""
    if isinstance(event, ObjectAddedEvent):
        print(f"[Temperature added] '{event.obj.name}' ({event.obj.id})")

    elif isinstance(event, ObjectUpdatedEvent):
        print(f"[Temperature updated] '{event.obj.name}' ({event.obj.id})")
        for attr in event.attrs_changed:
            print(f"    {attr} = {getattr(event.obj, attr)}")


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    async with Vantage(args.host, args.username, args.password) as vantage:
        # Subscribe to updates for all sensors
        vantage.temperature_sensors.subscribe(callback)

        # Fetch all known sensors from the controller
        await vantage.temperature_sensors.initialize()

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
