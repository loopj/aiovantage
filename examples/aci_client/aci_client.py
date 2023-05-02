import asyncio
import os

from aiovantage.config_client import ConfigClient
from aiovantage.config_client.helpers import get_objects_by_type
from aiovantage.config_client.interfaces import IIntrospection
from aiovantage.config_client.methods.introspection import GetVersion
from aiovantage.config_client.system_objects import Area, Load, StationObject


# Set your Vantage host ip, username, and password as environment variables
VANTAGE_HOST = os.getenv("VANTAGE_HOST", "vantage.local")
VANTAGE_USER = os.getenv("VANTAGE_USER")
VANTAGE_PASS = os.getenv("VANTAGE_PASS")


async def main() -> None:
    async with ConfigClient(VANTAGE_HOST, VANTAGE_USER, VANTAGE_PASS) as client:
        # Simple RPC request without any params (IIntrospection.GetVersion)
        print("# Controller Versions")
        version = await client.request(IIntrospection, GetVersion)
        print(version)
        print()

        # Dump all Areas using the get_objects_by_type helper
        print("# Vantage Areas")
        async for area in get_objects_by_type(client, ["Area"], Area):
            print(area)
        print()

        # Dump all Loads using the get_objects_by_type helper
        print("# Vantage Loads")
        async for load in get_objects_by_type(client, ["Load"], Load):
            print(load)
        print()

        # Dump some StationObjects using the get_objects_by_type helper
        print("# Vantage Stations")
        async for station in get_objects_by_type(
            client, ["Keypad", "EqCtrl"], StationObject
        ):
            print(station)
        print()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
