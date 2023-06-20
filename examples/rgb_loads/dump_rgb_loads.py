"""Prints out the id and name of each RGB load in the Vantage controller."""

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
        async for rgb_load in vantage.rgb_loads:
            print(
                f"[{rgb_load.id}] '{rgb_load.name}' "
                f"is {'ON' if rgb_load.is_on else 'OFF'}"
            )


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)
