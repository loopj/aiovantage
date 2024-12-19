"""Dump all Vantage object types."""

import argparse
import asyncio
import contextlib
from pathlib import Path
from xml.etree import ElementTree

from aiovantage.config_client import ConfigClient
from aiovantage.config_client.interfaces.introspection import GetInterfaces, GetTypes
from aiovantage.discovery import get_controller_details

# Grab connection info from command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
args = parser.parse_args()

ElementTree.register_namespace("vntg", "http://www.vantagecontrols.com/Vantage")
ElementTree.register_namespace("xs", "http://www.w3.org/2001/XMLSchema")


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
    """Dump all Vantage object types."""
    controller = await get_controller_details(args.host)
    if controller is None:
        parser.print_usage()
        print(f"error: no Vantage controller found at {args.host}")
        return

    if controller.requires_auth and not (args.username or args.password):
        parser.print_usage()
        print("error: controller requires auth, but no username/password provided")
        return

    async with ConfigClient(
        args.host, args.username, args.password, ssl=controller.supports_ssl
    ) as client:
        # Dump all object type schemas
        types = await client.request(GetTypes)
        if types is None:
            print("error: IIntrospection.GetTypes returned None")
            return

        for object_type in types:
            try:
                schema = await get_type_info(client, object_type.name)
                file = Path(f"schemas/types/{object_type.name}.xsd")
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(schema, encoding="utf-8")
            except ElementTree.ParseError as exc:
                print(f"Failed to get type info for {object_type.name}: {exc}")

        # Dump all object interface definitions
        interfaces = await client.request(GetInterfaces)
        if interfaces is None:
            print("error: IIntrospection.GetInterfaces returned None")
            return

        for interface in interfaces:
            try:
                schema = await get_interface_info(client, interface.name)
                file = Path(f"schemas/interfaces/{interface.name}.idl")
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(schema, encoding="utf-8")
            except ElementTree.ParseError as exc:
                print(f"Failed to get interface info for {interface.name}: {exc}")

        print(f"Dumped types and interfaces to {Path.cwd() / 'schemas'}")


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
