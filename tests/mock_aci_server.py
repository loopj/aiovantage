# python3 -m tests.mock_aci_server

import asyncio
import socket
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Set, Type

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.parsers.handlers import XmlEventHandler
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from aiovantage.config_client.methods.configuration import (
    CloseFilter,
    GetFilterResults,
    ObjectChoice,
    OpenFilter,
)
from aiovantage.config_client.objects import SystemObject
from aiovantage.config_client.methods import Method, CallType, ReturnType

from .common import ObjectStore


class MockACISession:
    def __init__(
        self, writer: asyncio.StreamWriter, id: int, objects: ObjectStore
    ) -> None:
        self._writer = writer
        self._id = id
        self._objects = objects
        self._buffer = ""
        self._filter_results: Dict[int, List[SystemObject]] = {}
        self._handle = 0

        self._parser = XmlParser(
            config=ParserConfig(fail_on_unknown_properties=False),
            handler=XmlEventHandler,
        )

        self._serializer = XmlSerializer(
            config=SerializerConfig(xml_declaration=False),
        )

        print(f"Client {self._id} connected.")

    async def close(self) -> None:
        print(f"Client {self._id} disconnected.")

    def data_received(self, data: bytes) -> None:
        self._buffer += data.decode()

        try:
            root = ET.fromstring(self._buffer)
            response = self.handle_request(root) + "\n"
            self._writer.write(response.encode())
            self._buffer = ""
        except ET.ParseError:
            pass

    def open_filter(self, tree: ET.Element) -> str:
        params = self._unmarshall_request(OpenFilter, tree)
        assert params is not None

        object_types = params.objects.object_type if params.objects else []

        results: List[SystemObject] = []
        if "Load" in object_types:
            results.extend(list(self._objects.loads.values()))

        if "Area" in object_types:
            results.extend(list(self._objects.areas.values()))

        if "Keypad" in object_types:
            results.extend(list(self._objects.stations.values()))

        if "Button" in object_types:
            results.extend(list(self._objects.buttons.values()))

        if "DryContact" in object_types:
            results.extend(list(self._objects.dry_contacts.values()))

        self._handle += 1
        self._filter_results[self._handle] = results

        return self._marshall_response(OpenFilter, self._handle)

    def get_filter_results(self, tree: ET.Element) -> str:
        params = self._unmarshall_request(GetFilterResults, tree)
        assert params is not None

        handle = params.h_filter
        count = params.count

        results = []
        if handle in self._filter_results:
            results.extend(self._filter_results[handle][:count])
            del self._filter_results[handle][:count]

        return self._marshall_response(
            GetFilterResults,
            GetFilterResults.Return(
                objects=[ObjectChoice(id=obj.id, choice=obj) for obj in results]
            ),
        )

    def close_filter(self, tree: ET.Element) -> str:
        handle = self._unmarshall_request(CloseFilter, tree)
        assert handle is not None

        success = False
        if handle in self._filter_results:
            del self._filter_results[handle]
            success = True

        return self._marshall_response(CloseFilter, success)

    def handle_request(self, tree: ET.Element) -> str:
        interface_name = tree.tag
        method_name = tree[0].tag
        qualified_method_name = f"{interface_name}.{method_name}"

        print(f"Client {self._id} requested {qualified_method_name}")

        if qualified_method_name == "IConfiguration.OpenFilter":
            return self.open_filter(tree)
        elif qualified_method_name == "IConfiguration.GetFilterResults":
            return self.get_filter_results(tree)
        elif qualified_method_name == "IConfiguration.CloseFilter":
            return self.close_filter(tree)
        else:
            print(f"Client {self._id} requested unknown method {qualified_method_name}")

            return (
                f"<{interface_name}>\n"
                f"\t<{method_name}>\n"
                f"\t\t<return/>\n"
                f"\t</{method_name}>\n"
                f"</{interface_name}>"
            )

    def _unmarshall_request(
        self, method_cls: Type[Method[CallType, ReturnType]], tree: ET.Element
    ) -> Optional[CallType]:
        # Extract the method element from XML doc
        method_el = tree.find(f"{method_cls.__name__}")
        if method_el is None:
            raise ValueError(
                f"Request to {method_cls.interface} did not contain a "
                f"<{method_cls.__name__}> element"
            )

        # Parse the method element with xsdata
        method = self._parser.parse(method_el, method_cls)
        return method.call

    def _marshall_response(
        self, method_cls: Type[Method[CallType, ReturnType]], params: Any
    ) -> str:
        # Build the method object
        method = method_cls()
        method.return_value = params

        # Render the method object to XML with xsdata
        return (
            f"<{method.interface}>"
            f"{self._serializer.render(method)}"
            f"</{method.interface}>"
        )


class MockACIServer:
    def __init__(self) -> None:
        self._sessions: Set[MockACISession] = set()
        self._objects = ObjectStore()

    async def handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        session = MockACISession(writer, len(self._sessions) + 1, self._objects)
        self._sessions.add(session)

        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                session.data_received(data)
        finally:
            self._sessions.discard(session)
            await session.close()

    async def start(self) -> None:
        # Create the server
        server = await asyncio.start_server(
            self.handle_client, "localhost", 2001, family=socket.AF_INET
        )

        # Get the server address
        addr = server.sockets[0].getsockname()
        print(f"Mock ACI service started at {addr[0]}:{addr[1]}")

        # Run the server indefinitely
        async with server:
            await server.serve_forever()


server = MockACIServer()
asyncio.run(server.start())
