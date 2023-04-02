#!/usr/bin/env python3

from dataclasses import dataclass
from os.path import abspath, dirname
from sys import path

path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio
import logging

from aiovantage.clients.aci.client import ACIClient
from aiovantage.xml_dataclass import attr_field, element_field, from_xml_el

logging.basicConfig(level=logging.INFO)


@dataclass
class Area:
    id: int = attr_field(name="VID")
    name: str = element_field(name="Name")


@dataclass
class Load:
    id: int = attr_field(name="VID")
    name: str = element_field(name="Name")


async def main() -> None:
    async with ACIClient("10.2.0.103", "administrator", "ZZuUw76CnL") as client:
        # Get version
        print("# System Version Information")
        version = await client.introspection.get_version()
        print(version)
        print()

        # Dump all areas
        print("# Vantage Areas")
        async for area in client.configuration.get_objects(["Area"]):
            print(from_xml_el(area, Area))
        print()

        # Dump all loads
        print("# Vantage Loads")
        async for area in client.configuration.get_objects("Load"):
            print(from_xml_el(area, Load))
        print()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
