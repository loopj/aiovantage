import asyncio
import datetime
import logging
import ssl
import xml.etree.ElementTree as ET
from types import TracebackType
from typing import Any, Optional, Type

from aiovantage.clients.aci.configuration import Configuration
from aiovantage.clients.aci.introspection import Introspection
from aiovantage.clients.aci.login import Login
from aiovantage.xml_dataclass import to_xml_el, DataclassInstance


class ACIClient:
    """Communicate with a Vantage InFusion Application Communication Interface service.

    The ACI service is an XML-based RPC service that Design Center uses to communicate with
    Vantage Controllers. There are a number of interfaces exposed, each with one or more methods.

    We're using this service to get a list of all available Vantage objects known by the
    controller, but it should be a fairly capable client for all RPC-like requests to the ACI
    service.
    """

    def __init__(
        self,
        host: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_ssl: bool = True,
        port: Optional[int] = None,
    ):
        self._host = host
        self._username = username
        self._password = password
        self._use_ssl = use_ssl
        self._logger = logging.getLogger(__name__)
        self._connection: Optional[tuple[asyncio.StreamReader, asyncio.StreamWriter]] = None
        self._timeout = 5

        if port is None:
            self._port = 2010 if use_ssl else 2001
        else:
            self._port = port

        if use_ssl:
            self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)

    async def __aenter__(self) -> "ACIClient":
        """Return Context manager."""
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Close context manager."""
        await self.close()

    @property
    def login(self) -> Login:
        return Login(self)

    @property
    def introspection(self) -> Introspection:
        return Introspection(self)

    @property
    def configuration(self) -> Configuration:
        return Configuration(self)

    async def connect(self) -> None:
        """Connect to the ACI service and authenticate if necessary."""

        # Connect
        self._connection = await asyncio.open_connection(
            self._host, self._port, ssl=self._ssl_context, limit=1024 * 1024 * 10
        )
        self._logger.info("Connected")

        # Authenticate (if required)
        if self._username is None or self._password is None:
            return

        # Make the login request
        response = await self.login.login(self._username, self._password)
        if response.success:
            self._logger.info("Login successful")
        else:
            raise Exception("Login failed")

    async def close(self) -> None:
        """Close the connection."""
        if self._connection is None:
            return

        _, writer = self._connection
        writer.close()
        await writer.wait_closed()

        self._connection = None

    async def request(
        self, interface: str, method: str, params: Optional[DataclassInstance] = None
    ) -> ET.Element:
        """Build and send an RPC request."""

        if self._connection is None:
            raise RuntimeError("Not connected")

        request_el = ET.Element(interface)
        method_el = ET.SubElement(request_el, method)
        if params is not None:
            method_el.append(to_xml_el(params, "call"))
        else:
            ET.SubElement(method_el, "call")

        # Send the request
        reader, writer = self._connection
        request = ET.tostring(request_el)
        writer.write(request)
        await writer.drain()

        # Fetch the response
        buffer = bytearray()
        while True:
            try:
                chunk = await asyncio.wait_for(reader.read(100), self._timeout)
            except asyncio.TimeoutError:
                raise Exception("RPC call failed, timed out waiting for response")

            if chunk == b'':
                break

            if chunk == b'\x18':
                raise RuntimeError(f"RPC call failed, received CAN (0x18) byte. Malformed request to '{interface}.{method}'?")

            buffer.extend(chunk)

            if f"</{interface}>".encode() in buffer or f"<{interface}/>".encode() in buffer:
                break

        # Parse the response
        response = buffer.decode()
        response_el = ET.fromstring(response)

        # Make sure the response is valid
        el = response_el.find(f"{method}/return")
        if el is None:
            raise Exception(f"RPC call failed, no <return> element in response: {response}")

        return el