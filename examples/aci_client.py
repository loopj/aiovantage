#!/usr/bin/env python3

from dataclasses import dataclass
from os.path import abspath, dirname
from sys import path

path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio
import logging

from aiovantage.clients.aci import ACIClient
from aiovantage.models.xml_model import XMLModel, attr, element

logging.basicConfig(level=logging.INFO)


@dataclass
class GetVersion(XMLModel):
    kernel: str = element()
    rootfs: str = element()
    app: str = element()


@dataclass
class Load(XMLModel):
    id: int = attr(alias="VID")
    name: str = element(alias="Name")


@dataclass
class Area(XMLModel):
    id: int = attr(alias="VID")
    name: str = element(alias="Name")


async def main() -> None:
    async with ACIClient("10.2.0.103", "administrator", "ZZuUw76CnL") as client:
        # Raw RPC request example (IIIntrospection.GetVersion)
        resp = await client.request("IIntrospection", "GetVersion")
        version = GetVersion.from_xml_el(resp)
        print(version)
        print()

        # Fetch known loads using built-in fetch_objects method
        print("## Known Loads")
        objects = await client.fetch_objects(["Load"])
        loads = (Load.from_xml_el(el) for el in objects)
        for load in loads:
            print(load)
        print()

        # Fetch known loads using built-in fetch_objects method
        print("## Known Areas")
        objects = await client.fetch_objects(["Area"])
        areas = (Area.from_xml_el(el) for el in objects)
        for area in areas:
            print(area)
        print()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
