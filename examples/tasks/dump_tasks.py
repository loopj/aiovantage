"""Prints out the id, name, and running state of each task in the Vantage controller."""

import asyncio
import contextlib

from aiovantage import Vantage

from debug_logging import configure_logging, parse_arguments

# Grab connection info from command line arguments
args = parse_arguments()


async def main() -> None:
    """Run code example."""
    configure_logging(args.debug)

    # Connect to the Vantage controller and print out the name and value of each GMem
    async with Vantage(args.host, args.username, args.password) as vantage:
        async for task in vantage.tasks:
            print(f"[{task.id}] '{task.name}' is_running={task.is_running}")


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)
