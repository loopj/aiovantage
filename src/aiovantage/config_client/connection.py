"""Client for the Vantage Application Communication Interface (ACI) service."""

import asyncio
import logging
from ssl import CERT_NONE, SSLContext, create_default_context
from types import TracebackType
from typing import Any, Optional, Type, Union
from xml.etree import ElementTree

from typing_extensions import Self
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.parsers.handlers import XmlEventHandler
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from .errors import ClientConnectionError, ClientTimeoutError
from .methods import Call, Method, Return


class ConfigConnection:
    """A connection to the Vantage ACI service."""

    def __init__(
        self,
        host: str,
        port: Optional[int] = None,
        *,
        ssl: Union[SSLContext, bool] = True,
        conn_timeout: Optional[float] = 5,
        read_timeout: Optional[float] = 30,
    ) -> None:
        """Create a connection to the Vantage ACI service.

        Args:
            host: The hostname or IP address of the Vantage host.
            port: The port to connect to. Defaults to 3010 if SSL is enabled, else 3001.
            ssl: Whether to use SSL for the connection. If True, a default SSL context
                will be created. If False, SSL will not be used. If a SSLContext is
                provided, it will be used.
            conn_timeout: The timeout for establishing a connection, in seconds.
            read_timeout: The timeout for reading a response, in seconds.
        """

        self._host = host
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._lock = asyncio.Lock()
        self._logger = logging.getLogger(__name__)

        # Set up the SSL context
        self._ssl: Optional[SSLContext]
        if ssl is True:
            # We don't have a local issuer certificate to check against, and we'll be
            # connecting to an IP address so we can't check the hostname
            self._ssl = create_default_context()
            self._ssl.check_hostname = False
            self._ssl.verify_mode = CERT_NONE
        elif isinstance(ssl, SSLContext):
            self._ssl = ssl
        else:
            self._ssl = None

        # Set up the port
        self._port: int
        if port is None:
            self._port = 2010 if ssl else 2001
        else:
            self._port = port

        # Set up XML parser and serializer
        self._parser = XmlParser(
            config=ParserConfig(fail_on_unknown_properties=False),
            handler=XmlEventHandler,
        )

        self._serializer = XmlSerializer(
            config=SerializerConfig(xml_declaration=False),
        )

    async def __aenter__(self) -> Self:
        """Return context manager."""
        await self.open()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit context manager."""
        self.close()
        if exc_val:
            raise exc_val

    async def open(self) -> None:
        """Open a connection to the Vantage ACI service."""

        # If we're already connected, do nothing
        if self._writer is not None and not self._writer.is_closing():
            return

        # Create the connection
        try:
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(
                    self._host,
                    self._port,
                    ssl=self._ssl,
                    limit=2**20,
                ),
                timeout=self._conn_timeout,
            )
        except asyncio.TimeoutError as exc:
            raise ClientTimeoutError(
                f"Timed out connecting to {self._host}:{self._port}"
            ) from exc
        except OSError as exc:
            raise ClientConnectionError(
                f"Failed to connect to {self._host}:{self._port}"
            ) from exc

    def close(self) -> None:
        """Close the connection to the Vantage ACI service."""

        if self._writer is not None and not self._writer.is_closing():
            self._writer.close()
            self._writer = None

    @property
    def closed(self) -> bool:
        """Whether the connection is closed."""

        return self._writer is None or self._writer.is_closing()

    async def raw_request(self, interface: str, payload: str) -> str:
        """Send a plaintext request to the ACI service.

        Args:
            interface: The interface to send the request to
            payload: The request payload string to send

        Returns:
            The response payload string
        """

        # Make sure we're connected
        if self._reader is None or self._writer is None or self._writer.is_closing():
            raise ClientConnectionError("Not connected to Vantage ACI service")

        async with self._lock:
            try:
                # Send the request
                request = f"<{interface}>{payload}</{interface}>"
                self._logger.debug(request)
                self._writer.write(request.encode())
                await self._writer.drain()

                # Fetch the response
                end_bytes = f"</{interface}>\n".encode()
                data = await asyncio.wait_for(
                    self._reader.readuntil(end_bytes), timeout=self._read_timeout
                )

            except asyncio.TimeoutError as err:
                raise ClientTimeoutError from err
            except (OSError, asyncio.IncompleteReadError) as err:
                raise ClientConnectionError from err

            response = data.decode()
            self._logger.debug(response)

            return response

    async def request(
        self, method_cls: Type[Method[Call, Return]], params: Any = None
    ) -> Return:
        """Marshall a request, send it to the ACI service, and yield a parsed object.

        Args:
            method_cls: The method class to use
            params: The parameters instance to pass to the method

        Returns:
            The parsed response object
        """

        # Build the method object
        method = method_cls()
        method.call = params

        # Render the method object to XML with xsdata
        request = self._serializer.render(method)
        response = await self.raw_request(method.interface, request)

        # Parse the XML doc
        tree = ElementTree.fromstring(response)

        # Extract the method element from XML doc
        method_el = tree.find(f"{method_cls.__name__}")
        if method_el is None:
            raise ValueError(
                f"Response from {method_cls.interface} did not contain a "
                f"<{method_cls.__name__}> element"
            )

        # Parse the method element with xsdata
        method = self._parser.parse(method_el, method_cls)
        if method.return_value is None or method.return_value == "":
            raise TypeError(
                f"Response from {method_cls.interface}.{method_cls.__name__}"
                f" did not contain a return value"
            )

        return method.return_value
