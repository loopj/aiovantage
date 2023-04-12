#!/usr/bin/env python3

import asyncio
import logging
from typing import AsyncIterator, List, Type, TypeVar

from aiovantage.aci_client import ACIClient
from aiovantage.aci_client.interfaces import IConfiguration, IIntrospection
from aiovantage.aci_client.methods.configuration import (
    CloseFilter,
    GetFilterResults,
    ObjectFilter,
    OpenFilter,
)
from aiovantage.aci_client.methods.introspection import GetVersion
from aiovantage.aci_client.system_objects import Area, Load

logging.basicConfig(level=logging.INFO)


T = TypeVar("T")

async def get_objects(client: ACIClient, vantage_types: List[str], base_type: Type[T]) -> AsyncIterator[T]:
    # Open the filter
    handle = await client.request(
        IConfiguration,
        OpenFilter,
        OpenFilter.Params(objects=ObjectFilter(object_type=vantage_types)),
    )

    # Get the results
    while True:
        response = await client.request(
            IConfiguration,
            GetFilterResults,
            GetFilterResults.Params(h_filter=handle),
        )

        if not response.object_value:
            break

        for object in response.object_value:
            if object.choice and isinstance(object.choice, base_type):
                yield object.choice
            else:
                print(f"Couldnt parse object with vid {object.id}")

    # Close the filter
    await client.request(IConfiguration, CloseFilter, handle)


async def main() -> None:
    async with ACIClient("10.2.0.103", "administrator", "ZZuUw76CnL") as client:
        # Simple RPC request without any params (IIntrospection.GetVersion)
        print("# Controller Versions")
        version = await client.request(IIntrospection, GetVersion)
        print(version)
        print()

        # Dump all areas
        print("# Vantage Areas")
        async for obj in get_objects(client, ["Area"], Area):
            print(obj)
        print()

        # Dump all loads
        print("# Vantage Loads")
        async for obj in get_objects(client, ["Load"], Load):
            print(obj)
        print()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
