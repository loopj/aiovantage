#!/usr/bin/env python3

from dataclasses import dataclass
from os.path import abspath, dirname
from sys import path
from typing import Type, TypeVar

path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio
import logging
from xml.etree import ElementTree as ET

from aiovantage.clients.aci import ACIClient
from aiovantage.xml_dataclass import attr_field, element_field, text_field, from_xml_el, DataclassInstance

logging.basicConfig(level=logging.INFO)


@dataclass
class OpenFilterResponse:
    handle: int = text_field()


@dataclass
class GetFilterResultsResponse:
    objects: list[ET.Element] = element_field(name="Object", factory=lambda el, _: el[0], default=None)


@dataclass
class CloseFilterResponse:
    success: bool = text_field()


@dataclass
class GetVersionResponse:
    kernel: str = element_field()
    rootfs: str = element_field()
    app: str = element_field()


@dataclass
class Area:
    id: int = attr_field(name="VID")
    name: str = element_field(name="Name")


@dataclass
class Load:
    id: int = attr_field(name="VID")
    name: str = element_field(name="Name")


# IConfiguration.OpenFilter
async def IConfiguration_OpenFilter(conn: ACIClient, xpath: str | None = None) -> OpenFilterResponse:
    response = await conn.request("IConfiguration", "OpenFilter", {
        "Objects": None,
        "XPath": xpath,
    })
    return from_xml_el(response, OpenFilterResponse)


# IConfiguration.GetFilterResults
async def IConfiguration_GetFilterResults(conn: ACIClient, handle: int, per_page: int = 50, whole_object: bool = True) -> GetFilterResultsResponse:
    response = await conn.request("IConfiguration", "GetFilterResults", {
        "Count": per_page,
        "WholeObject": whole_object,
        "hFilter": handle,
    })
    return from_xml_el(response, GetFilterResultsResponse)


# IConfiguration.CloseFilter
async def IConfiguration_CloseFilter(conn: ACIClient, handle: int) -> CloseFilterResponse:
    response = await conn.request("IConfiguration", "CloseFilter", handle)
    return from_xml_el(response, CloseFilterResponse)


# IIntrospection.GetVersion
async def IIntrospection_GetVersion(conn: ACIClient) -> GetVersionResponse:
    response = await conn.request("IIntrospection", "GetVersion")
    return from_xml_el(response, GetVersionResponse)


# Fetch all objects of a given type, combining OpenFilter, GetFilterResults and CloseFilter
T = TypeVar("T", bound=DataclassInstance)
async def fetch_objects(conn: ACIClient, el_name: str, type: Type[T]) -> list[T]:
    open_filter_response = await IConfiguration_OpenFilter(conn, f"/{el_name}")

    objects = []
    while True:
        filter_results_response = await IConfiguration_GetFilterResults(conn, open_filter_response.handle, per_page=50)
        if not filter_results_response.objects:
            break

        for el in filter_results_response.objects:
            objects.append(from_xml_el(el, type))

    await IConfiguration_CloseFilter(conn, open_filter_response.handle)

    return objects


async def main() -> None:
    async with ACIClient("10.2.0.103", "administrator", "ZZuUw76CnL") as client:
        # Get version
        version_response = await IIntrospection_GetVersion(client)
        print(version_response)
        print()

        # Dump all areas
        print("# Vantage Areas")
        areas = await fetch_objects(client, "Area", Area)
        for area in areas:
            print(area.name)
        print()

        # Dump all loads
        print("# Vantage Loads")
        loads = await fetch_objects(client, "Load", Load)
        for load in loads:
            print(load.name)
        print()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
