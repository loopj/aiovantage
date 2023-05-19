# python3 -m tests.mock_aci_server

import asyncio
import socket
import xml.etree.ElementTree as ET
from typing import Dict, List, Set

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
        method = OpenFilter
        params = self._parser.parse(tree, method).call
        assert params is not None

        object_types = params.objects.object_type if params.objects else []

        results: List[SystemObject] = []
        if "Load" in object_types:
            results.extend(list(self._objects.loads.values()))

        if "Area" in object_types:
            results.extend(list(self._objects.areas.values()))

        if "Keypad" in object_types:
            results.extend(list(self._objects.stations.values()))

        self._handle += 1
        self._filter_results[self._handle] = results

        method_str = self._serializer.render(OpenFilter(return_value=self._handle))

        return f"<{method.interface}>{method_str}</{method.interface}>"

    def get_filter_results(self, tree: ET.Element) -> str:
        method = GetFilterResults
        params = self._parser.parse(tree, method).call
        assert params is not None

        handle = params.h_filter
        count = params.count

        results = []
        if handle in self._filter_results:
            results.extend(self._filter_results[handle][:count])
            del self._filter_results[handle][:count]

        method_str = self._serializer.render(
            GetFilterResults(
                return_value=GetFilterResults.Return(
                    objects=[ObjectChoice(id=obj.id, choice=obj) for obj in results]
                )
            )
        )

        return f"<{method.interface}>{method_str}</{method.interface}>"

    def close_filter(self, tree: ET.Element) -> str:
        method = CloseFilter
        handle = self._parser.parse(tree, method).call
        assert handle is not None

        success = False
        if handle in self._filter_results:
            del self._filter_results[handle]
            success = True

        method_str = self._serializer.render(CloseFilter(return_value=success))

        return f"<{method.interface}>{method_str}</{method.interface}>"

    def handle_request(self, tree: ET.Element) -> str:
        interface_name = tree.tag
        method_name = tree[0].tag
        qualified_method_name = f"{interface_name}.{method_name}"

        print(f"Client {self._id} requested {qualified_method_name}")

        if qualified_method_name == "IConfiguration.OpenFilter":
            return self.open_filter(tree[0])
        elif qualified_method_name == "IConfiguration.GetFilterResults":
            return self.get_filter_results(tree[0])
        elif qualified_method_name == "IConfiguration.CloseFilter":
            return self.close_filter(tree[0])
        else:
            print(f"Client {self._id} requested unknown method {qualified_method_name}")

            return (
                f"<{interface_name}>\n"
                f"\t<{method_name}>\n"
                f"\t\t<return/>\n"
                f"\t</{method_name}>\n"
                f"</{interface_name}>"
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
