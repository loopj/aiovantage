import asyncio
import datetime
import logging
import ssl
import xml.etree.ElementTree as ET
from collections.abc import Iterable
from types import TracebackType
from typing import Any, Type


class ACIClient:
    """Communicate with a Vantage InFusion ACI (Application Communication Interface) service.

    The ACI service is an XML-based RPC service that Design Center uses to communicate with
    Vantage Controllers. There are a number of interfaces exposed, each with one or more methods.

    We're using this service to get a list of all available Vantage objects known by the
    controller, but it should be a fairly capable client for all RPC-like requests to the ACI
    service.
    """

    def __init__(
        self,
        host: str,
        username: str | None = None,
        password: str | None = None,
        use_ssl: bool = True,
        port: int | None = None,
    ):
        self._host = host
        self._username = username
        self._password = password
        self._use_ssl = use_ssl
        self._logger = logging.getLogger(__name__)
        self._connection: tuple[asyncio.StreamReader, asyncio.StreamWriter] | None = None

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
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close context manager."""
        await self.close()

    async def connect(self) -> None:
        """Connect to the ACI service and authenticate if necessary."""

        # Connect
        self._connection = await asyncio.open_connection(
            self._host, self._port, ssl=self._ssl_context, limit=1024 * 1024 * 10
        )
        self._logger.info("Connected")

        # Authenticate (if required)
        await self._login()

    async def close(self) -> None:
        """Close the connection."""
        if self._connection is None:
            return

        _, writer = self._connection
        writer.close()
        await writer.wait_closed()

        self._connection = None

    async def request(
        self, interface: str, method: str, params: Any = None
    ) -> ET.Element:
        """Build and send an RPC request."""

        if self._connection is None:
            raise RuntimeError("Not connected")

        def _params_to_xml(data: dict, parent: ET.Element) -> ET.Element:
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        for item in value:
                            element = ET.SubElement(parent, key)
                            _params_to_xml(item, element)
                    else:
                        element = ET.SubElement(parent, key)
                        _params_to_xml(value, element)
            elif isinstance(data, bool):
                parent.text = str(data).lower()
            elif isinstance(data, datetime.datetime):
                parent.text = data.isoformat(timespec="seconds")
            elif data is not None:
                parent.text = str(data)

            return parent

        # Build the RPC request
        request_el = ET.Element(interface)
        method_el = ET.SubElement(request_el, method)
        params_el = ET.SubElement(method_el, "call")
        _params_to_xml(params, params_el)

        reader, writer = self._connection

        # Send the request
        request = ET.tostring(request_el)
        # self._logger.debug(request.decode())
        writer.write(request)
        await writer.drain()

        # Fetch the response
        data = await reader.readuntil(f"</{interface}>".encode())
        response = data.decode()
        # self._logger.debug(response)

        # Parse the response
        response_el = ET.fromstring(response)
        el = response_el.find(f"{method}/return")
        if el is None:
            raise Exception("RPC call failed (unknown response)")

        return el

    async def fetch_objects(
        self, object_types: Iterable[str] | None = None, per_page: int = 50
    ) -> Iterable[ET.Element]:
        # Build the weird "XPath" query
        xpath = None
        if object_types is not None:
            xpath = " or ".join([f"/{str}" for str in object_types])

        # Create a filter
        response = await self.request(
            "IConfiguration",
            "OpenFilter",
            {
                "Objects": None,
                "XPath": xpath,
            },
        )
        handle = response.text

        # Get results from filter handle
        results = []
        while True:
            response = await self.request(
                "IConfiguration",
                "GetFilterResults",
                {
                    "Count": per_page,
                    "WholeObject": True,
                    "hFilter": handle,
                },
            )

            objects = response.findall(f"Object/*")
            if len(objects) > 0:
                results.extend(objects)
            else:
                break

        # Close filter handle
        await self.request("IConfiguration", "CloseFilter", handle)

        # Return objects we care about
        return results

    async def _login(self) -> None:
        if self._username is None or self._password is None:
            return

        # Send login command
        response = await self.request(
            "ILogin",
            "Login",
            {
                "User": self._username,
                "Password": self._password,
            },
        )

        # Validate response
        if response.text == "false":
            raise Exception("Login failed")
        else:
            self._logger.info("Login successful")
