"""Print a list of all loads that are currently on every 5 seconds."""

import asyncio
import contextlib

from aiovantage import Vantage

from debug_logging import configure_logging, parse_arguments

# Grab connection info from command line arguments
args = parse_arguments()


async def main() -> None:
    """Run code example."""
    configure_logging(args.debug)

    async with Vantage(args.host, args.username, args.password) as vantage:
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
    asyncio.run(main(), debug=args.debug)
