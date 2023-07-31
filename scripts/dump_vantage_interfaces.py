"""Dump all Vantage object interfaces."""
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

ElementTree.register_namespace("", "http://www.vantagecontrols.com/Vantage")


async def get_interfaces(client: ConfigClient) -> List[str]:
    """Get a list of all available system object types."""
    response = await client.raw_request(
        "IIntrospection", "<GetInterfaces><call/></GetInterfaces>"
    )

    root = ElementTree.fromstring(response)
    return_el = root.find("./GetInterfaces/return")
    assert return_el is not None

    types = []
    for type_el in return_el:
        name = type_el.findtext("./Name")
        if name:
            types.append(name)

    return types


async def get_interface_info(client: ConfigClient, interface: str) -> str:
    """Get the XML schema for the specified object types."""
    response = await client.raw_request(
        "IIntrospection",
        f"<GetInterfaceInfo><call><Interface>{interface}</Interface></call></GetInterfaceInfo>",
    )

    root = ElementTree.fromstring(
        response,
        parser=ElementTree.XMLParser(
            target=ElementTree.TreeBuilder(insert_pis=True, insert_comments=True)
        ),
    )
    return_el = root.find("./GetInterfaceInfo/return/InterfaceInfo")
    assert return_el is not None

    doc = '<?xml version="1.0" encoding="UTF-8"?>\n'
    for child in return_el:
        doc += ElementTree.tostring(child, encoding="unicode")
    return doc


async def main() -> None:
    """Dump all Vantage object interfaces."""
    async with ConfigClient(args.host, args.username, args.password) as client:
        interfaces = await get_interfaces(client)
        for interface in interfaces:
            try:
                schema = await get_interface_info(client, interface)
                file = Path(f"interfaces/{interface}.vidl")
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(schema, encoding="utf-8")
            except ElementTree.ParseError as exc:
                print(f"Failed to get interface for {interface}: {exc}")


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
