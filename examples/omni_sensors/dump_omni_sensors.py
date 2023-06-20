"""Prints out the id, name, and level of each omni sensor in the Vantage controller."""

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
        async for omni_sensor in vantage.omni_sensors:
            level = f"{omni_sensor.level}" if omni_sensor.level is not None else "?"
            print(f"[{omni_sensor.id}] '{omni_sensor.name}' = {level}")


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)
