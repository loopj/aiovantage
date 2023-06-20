"""Prints out the id, name, and labels of each button in the Vantage controller."""

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
        async for button in vantage.buttons:
            print(
                f"[{button.id}] name='{button.name}' "
                f"text1='{button.text1}' text2='{button.text2}'"
            )


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)
