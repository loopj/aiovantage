"""Prints out the id, name and members of each blind group in the Vantage controller."""

import asyncio
import contextlib

from aiovantage import Vantage

from debug_logging import configure_logging, parse_arguments

# Grab connection info from command line arguments
args = parse_arguments()


async def main() -> None:
    """Run code example."""
    configure_logging(args.debug)

    # Connect to the Vantage controller and print out details of each blind group
    async with Vantage(args.host, args.username, args.password) as vantage:
        async for blind_group in vantage.blind_groups:
            print(f"[{blind_group.id}] '{blind_group.name}'")
            async for blind in vantage.blind_groups.blinds(blind_group.id):
                print(f"    [{blind.id}] '{blind.name}'")


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)
