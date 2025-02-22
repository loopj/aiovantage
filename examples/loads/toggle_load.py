"""Toggle a load on or off by ID."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage import Vantage

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("id", help="load id to toggle")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
parser.add_argument("--ssl", action=argparse.BooleanOptionalAction, default=True)
args = parser.parse_args()


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Connect to the Vantage controller
    async with Vantage(
        args.host, args.username, args.password, ssl=args.ssl
    ) as vantage:
        # Look up the load
        try:
            load_id = int(args.id)
        except ValueError:
            print("Invalid load id")
            return

        load = await vantage.loads.aget(load_id)
        if load is None:
            print("Load not found")
            return

        # Toggle the load
        print(f"Toggling {load.name} (id = {load.id})")
        if load.is_on:
            await load.turn_off()
        else:
            await load.turn_on()


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
