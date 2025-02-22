"""Example of using the get_objects helper to dump all objects of a given type."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage.config_client import ConfigClient, ConfigurationInterface

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
parser.add_argument("--ssl", action=argparse.BooleanOptionalAction, default=True)
args = parser.parse_args()


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    async with ConfigClient(
        args.host, args.username, args.password, ssl=args.ssl
    ) as client:
        # Dump all Areas using the get_objects helper
        print("# Vantage Areas")
        async for area in ConfigurationInterface.get_objects(client, "Area"):
            print(area)
        print()

        # Dump all Loads using the get_objects helper
        print("# Vantage Loads")
        async for load in ConfigurationInterface.get_objects(client, "Load"):
            print(load)
        print()

        # Dump some StationObjects using the get_objects helper
        print("# Vantage Stations")
        async for station in ConfigurationInterface.get_objects(
            client, "Keypad", "EqCtrl"
        ):
            print(station)
        print()


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
