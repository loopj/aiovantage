"""Example of using the get_objects helper to dump all objects of a given type."""

import asyncio
import contextlib

from aiovantage.config_client import ConfigClient
from aiovantage.config_client.helpers import get_objects

from debug_logging import configure_logging, parse_arguments

# Grab connection info from command line arguments
args = parse_arguments()


async def main() -> None:
    """Run code example."""
    configure_logging(args.debug)

    async with ConfigClient(args.host, args.username, args.password) as client:
        # Dump all Areas using the get_objects helper
        print("# Vantage Areas")
        async for area in get_objects(client, types="Area"):
            print(area)
        print()

        # Dump all Loads using the get_objects helper
        print("# Vantage Loads")
        async for load in get_objects(client, types="Load"):
            print(load)
        print()

        # Dump some StationObjects using the get_objects helper
        print("# Vantage Stations")
        async for station in get_objects(client, types=("Keypad", "EqCtrl")):
            print(station)
        print()


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)
