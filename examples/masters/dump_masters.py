"""Prints out the id, name, and serial number of each Vantage controller."""

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

    # Connect to the Vantage controller
    async with Vantage(args.host, args.username, args.password) as vantage:
        # Print out the id and name of each Vantage controller
        async for master in vantage.masters:
            print(
                f"[{master.vid}] '{master.name}' "
                f"serial_number={master.serial_number} "
                f"firmware_version={master.firmware_version}"
            )


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
