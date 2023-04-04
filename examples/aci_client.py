#!/usr/bin/env python3

from dataclasses import dataclass, field
from os.path import abspath, dirname
from sys import path

path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio
import logging
import xml.etree.ElementTree as ET
from typing import AsyncIterator

from aiovantage.clients.aci.client import ACIClient
from aiovantage.clients.aci.interfaces.configuration import (
    close_filter,
    get_filter_results,
    open_filter,
)
from aiovantage.clients.aci.interfaces.introspection import get_version

logging.basicConfig(level=logging.INFO)


@dataclass
class Area:
    id: int = field(metadata=dict(name="VID", type="Attribute"))
    name: str = field(metadata=dict(name="Name", type="Element"))


@dataclass
class Load:
    id: int = field(metadata=dict(name="VID", type="Attribute"))
    name: str = field(metadata=dict(name="Name", type="Element"))


async def get_objects(client: ACIClient, type: str) -> AsyncIterator[ET.Element]:
    response = await open_filter(client, f"/{type}")
    handle = response.handle

    while True:
        response = await get_filter_results(client, handle) # type: ignore
        if not response:
            break

        for obj in response: # type: ignore
            yield obj[0]

    await close_filter(client, handle)


async def main() -> None:
    async with ACIClient("10.2.0.103", "administrator", "ZZuUw76CnL") as client:
        # Get version
        print("# System Version Information")
        version = await get_version(client)
        print(version)
        print()

        # Dump all areas
        print("# Vantage Areas")
        async for obj in get_objects(client, "Area"):
            print(client._parse_object(obj, Area))
        print()

        # Dump all loads
        print("# Vantage Loads")
        async for obj in get_objects(client, "Load"):
            print(client._parse_object(obj, Load))
        print()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
