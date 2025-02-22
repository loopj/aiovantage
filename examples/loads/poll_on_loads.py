"""Print a list of all loads that are currently on every 5 seconds."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage import Vantage

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
parser.add_argument("--ssl", action=argparse.BooleanOptionalAction, default=True)
args = parser.parse_args()


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    async with Vantage(
        args.host, args.username, args.password, ssl=args.ssl
    ) as vantage:
        # Preload the loads from the controller
        await vantage.loads.initialize()

        # Print a list of all loads that are currently on every 5 seconds
        while True:
            on_loads = list(vantage.loads.on)
            print(f"{len(on_loads)} loads are ON")
            for load in on_loads:
                print(f"- {load.name}")
            print()

            await asyncio.sleep(5)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
