"""Dump all Vantage object types."""
import argparse
import asyncio
import contextlib
from pathlib import Path
from typing import List
from xml.etree import ElementTree

from aiovantage.config_client import ConfigClient

# Grab connection info from command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
args = parser.parse_args()

ElementTree.register_namespace("vntg", "http://www.vantagecontrols.com/Vantage")
ElementTree.register_namespace("xs", "http://www.w3.org/2001/XMLSchema")


async def get_types(client: ConfigClient) -> List[str]:
    """Get a list of all available system object types."""
    response = await client.raw_request(
        "IIntrospection", "<GetTypes><call/></GetTypes>"
    )

    root = ElementTree.fromstring(response)
    return_el = root.find("./GetTypes/return")
    assert return_el is not None

    types = []
    for type_el in return_el:
        name = type_el.findtext("./Name")
        if name:
            types.append(name)

    return types


async def get_type_info(client: ConfigClient, object_type: str) -> str:
    """Get the XML schema for the specified object types."""
    response = await client.raw_request(
        "IIntrospection",
        f"<GetTypeInfo><call><Type>{object_type}</Type></call></GetTypeInfo>",
    )

    root = ElementTree.fromstring(
        response,
        parser=ElementTree.XMLParser(
            target=ElementTree.TreeBuilder(insert_pis=True, insert_comments=True)
        ),
    )
    return_el = root.find("./GetTypeInfo/return/TypeInfo")
    assert return_el is not None

    doc = '<?xml version="1.0" encoding="UTF-8"?>\n'
    for child in return_el:
        doc += ElementTree.tostring(child, encoding="unicode")
    return doc


async def main() -> None:
    """Dump all Vantage object types."""
    async with ConfigClient(args.host, args.username, args.password) as client:
        object_types = await get_types(client)
        for object_type in object_types:
            try:
                schema = await get_type_info(client, object_type)
                file = Path(f"types/{object_type}.xsd")
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(schema, encoding="utf-8")
            except ElementTree.ParseError as exc:
                print(f"Failed to get schema for {object_type}: {exc}")


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
