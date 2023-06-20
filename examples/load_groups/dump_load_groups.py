"""Prints out the id, name, and members of each load group in the Vantage controller."""

import asyncio
import contextlib

from aiovantage import Vantage

from debug_logging import configure_logging, parse_arguments

# Grab connection info from command line arguments
args = parse_arguments()


async def main() -> None:
    """Run code example."""
    configure_logging(args.debug)

    # Connect to the Vantage controller and print out the name and level of each load
    async with Vantage(args.host, args.username, args.password) as vantage:
        async for load_group in vantage.load_groups:
            print(load_group)
            print(f"[{load_group.id}] '{load_group.name}' {load_group.load_ids}")


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)
