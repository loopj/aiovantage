#!/usr/bin/env python3

from os.path import abspath, dirname
from sys import path

path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio
import logging

from aiovantage.clients.aci import ACIClient

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    async with ACIClient("10.2.0.103", "administrator", "ZZuUw76CnL") as client:
        # Generic RPC request
        resp = await client.request("IIntrospection", "GetVersion")
        app_version = resp.find("app").text
        print("## Vantage App Version")
        print(app_version)
        print()

        # Built-in object fetch requests
        print("## Known Loads")
        objects = await client.fetch_objects(["Load"])
        for el in objects:
            print(el.find("Name").text)
        print()

        print("## Known Areas")
        objects = await client.fetch_objects(["Area"])
        for el in objects:
            print(el.find("Name").text)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
