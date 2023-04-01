#!/usr/bin/env python3

from dataclasses import dataclass
from os.path import abspath, dirname
from sys import path

path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio
import logging

from aiovantage.clients.aci import ACIClient
from aiovantage.xml_dataclass import attr_field, element_field, from_xml_el

logging.basicConfig(level=logging.INFO)


@dataclass
class GetVersion:
    kernel: str = element_field()
    rootfs: str = element_field()
    app: str = element_field()


@dataclass
class Load:
    id: int = attr_field(name="VID")
    name: str = element_field(name="Name")


@dataclass
class Area:
    id: int = attr_field(name="VID")
    name: str = element_field(name="Name")


async def main() -> None:
    async with ACIClient("10.2.0.103", "administrator", "ZZuUw76CnL") as client:
        # Raw RPC request example (IIIntrospection.GetVersion)
        resp = await client.request("IIntrospection", "GetVersion")
        version = from_xml_el(resp, GetVersion)
        print(version)
        print()

        # Fetch known loads using built-in fetch_objects method
        print("## Known Loads")
        objects = await client.fetch_objects(["Load"])
        loads = (from_xml_el(el, Load) for el in objects)
        for load in loads:
            print(load)
        print()

        # Fetch known loads using built-in fetch_objects method
        print("## Known Areas")
        objects = await client.fetch_objects(["Area"])
        areas = (from_xml_el(el, Area) for el in objects)
        for area in areas:
            print(area)
        print()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
