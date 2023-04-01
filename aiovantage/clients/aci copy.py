import asyncio
import datetime
import logging
import ssl
import xml.etree.ElementTree as ET
from collections import deque
from collections.abc import AsyncIterator, Iterable
from contextlib import asynccontextmanager
from types import TracebackType
from typing import Any, Type


class ACIConnection:
    def __init__(
        self,
        host: str,
        username: str | None,
        password: str | None,
        use_ssl: bool = True,
        port: int | None = None,
    ):
        self._host = host
        self._username = username
        self._password = password
        self._reader: asyncio.StreamReader
        self._writer: asyncio.StreamWriter
        self._logger = logging.getLogger(__name__)

        if port is None:
            self._port = 2010 if use_ssl else 2001
        else:
            self._port = port

        if use_ssl:
            self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)

    async def connect(self) -> None:
        """Connect to the ACI service."""
        self._reader, self._writer = await asyncio.open_connection(
            self._host, self._port, ssl=self._ssl_context
        )

        await self.login()

    async def close(self) -> None:
        """Close the connection."""
        self._writer.close()
        await self._writer.wait_closed()

    def _build_request(self, data: dict[str, Any], parent: ET.Element) -> ET.Element:
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    for item in value:
                        element = ET.SubElement(parent, key)
                        self._build_request(item, element)
                else:
                    element = ET.SubElement(parent, key)
                    self._build_request(value, element)
        elif isinstance(data, bool):
            parent.text = str(data).lower()
        elif isinstance(data, datetime.datetime):
            parent.text = data.isoformat(timespec="seconds")
        elif data is not None:
            parent.text = str(data)

        return parent

    async def request(
        self, interface: str, method: str, params: Any = None
    ) -> ET.Element:
        """Build and send an RPC request."""
        # Build the RPC request
        request_el = ET.Element(interface)
        method_el = ET.SubElement(request_el, method)
        params_el = ET.SubElement(method_el, "call")
        self._build_request(params, params_el)

        # Send the request
        request = ET.tostring(request_el)
        self._writer.write(request)
        await self._writer.drain()

        # Fetch the response
        data = await self._reader.readuntil(f"</{interface}>".encode())
        response = data.decode()

        # Parse the response
        response_el = ET.fromstring(response)
        el = response_el.find(f"{method}/return")
        if el is None:
            raise Exception("RPC call failed (unknown response)")

        return el

    async def login(self) -> None:
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


class ACIClient:
    def __init__(
        self,
        host: str,
        username: str | None = None,
        password: str | None = None,
        use_ssl: bool = True,
        port: int | None = None,
        pool_size: int = 10,
    ):
        self._host = host
        self._username = username
        self._password = password
        self._use_ssl = use_ssl
        self._port = port

        self._pool_size = pool_size
        self._connections: deque[ACIConnection] = deque()
        self._semaphore: asyncio.Semaphore = asyncio.Semaphore(pool_size)

        self._logger = logging.getLogger(__name__)

    async def __aenter__(self) -> "ACIClient":
        """Return Context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close context manager."""
        await self.close()

    async def _create_connection(self) -> ACIConnection:
        connection = ACIConnection(
            self._host,
            self._username,
            self._password,
            self._use_ssl,
            self._port,
        )
        await connection.connect()
        return connection

    async def _acquire(self) -> ACIConnection:
        await self._semaphore.acquire()

        if self._connections:
            return self._connections.popleft()

        return await self._create_connection()

    async def _release(self, connection: ACIConnection) -> None:
        self._connections.append(connection)
        self._semaphore.release()

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[ACIConnection]:
        connection = await self._acquire()
        try:
            yield connection
        finally:
            await self._release(connection)

    async def close(self) -> None:
        while self._connections:
            connection = self._connections.pop()
            await connection.close()

    async def request(
        self, interface: str, method: str, params: Any = None
    ) -> ET.Element:
        async with self.connection() as connection:
            return await connection.request(interface, method, params)

    async def fetch_objects(
        self, object_types: Iterable[str] | None = None, per_page: int = 100
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
