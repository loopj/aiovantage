#!/usr/bin/env python3

import asyncio
import logging

from aiovantage.aci_client import ACIClient
from aiovantage.aci_client.helpers import get_objects_by_type
from aiovantage.aci_client.interfaces import IIntrospection
from aiovantage.aci_client.methods.introspection import GetVersion
from aiovantage.aci_client.system_objects import Area, Load, StationObject

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    async with ACIClient("10.2.0.103", "administrator", "ZZuUw76CnL") as client:
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
