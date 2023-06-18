"""Prints out the id and name of each RGB load in the Vantage controller."""

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
args = parser.parse_args()


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Connect to the Vantage controller and print out the name and level of each load
    async with Vantage(args.host, args.username, args.password) as vantage:
        async for rgb_load in vantage.rgb_loads:
            print(
                f"[{rgb_load.id}] '{rgb_load.name}' "
                f"is {'ON' if rgb_load.is_on else 'OFF'}"
            )


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
