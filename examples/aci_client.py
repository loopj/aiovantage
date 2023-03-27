#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from os.path import abspath, dirname
from sys import path
from typing import Optional

path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio
import logging

from aiovantage.clients.aci import ACIClient

logging.basicConfig(level=logging.INFO)

def get_element_text(el: ET.Element, tag: str) -> Optional[str]:
    child = el.find(tag)
    return child.text if child is not None else None

async def main() -> None:
    async with ACIClient("10.2.0.103", "administrator", "ZZuUw76CnL") as client:
        # Generic RPC request
        resp = await client.request("IIntrospection", "GetVersion")
        print("## Vantage App Version")
        print(get_element_text(resp, "app"))
        print()

        # Built-in object fetch requests
        print("## Known Loads")
        objects = await client.fetch_objects(["Load"])
        for el in objects:
            print(get_element_text(el, "Name"))
        print()

        print("## Known Areas")
        objects = await client.fetch_objects(["Area"])
        for el in objects:
            print(get_element_text(el, "Name"))


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
