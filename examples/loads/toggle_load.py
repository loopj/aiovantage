"""Toggle a load on or off by ID."""

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
        try:
            load_id = int(args.id)
        except ValueError:
            print("Invalid load id")
            return

        load = await vantage.loads.aget(load_id)
        if load is None:
            print("Load not found")
            return

        print(f"Toggling {load.name} (id = {load.id})")
        if load.is_on:
            await vantage.loads.turn_off(load.id)
        else:
            await vantage.loads.turn_on(load.id)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)
