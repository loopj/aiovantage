"""Prints out the id, name, and serial number of each power profile."""

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

    # Connect to the Vantage controller
    async with Vantage(
        args.host, args.username, args.password, ssl=args.ssl
    ) as vantage:
        # Print out the id and name of each power profile
        async for profile in vantage.power_profiles:
            print(
                f"[{profile.id}] '{profile.name}' min={profile.min} max={profile.max}"
            )


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
