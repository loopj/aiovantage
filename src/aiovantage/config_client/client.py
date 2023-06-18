"""Client for the Vantage Application Communication Interface (ACI) service."""

import asyncio
import logging
import ssl
import xml.etree.ElementTree as ET
from types import TracebackType
from typing import Any, Optional, Tuple, Type, Union

from typing_extensions import Self
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.parsers.handlers import XmlEventHandler
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from .errors import ClientConnectionError, ClientTimeoutError
from .methods import Call, Method, Return
from .methods.login import Login

# Type alias for connections
Connection = Tuple[asyncio.StreamReader, asyncio.StreamWriter]


class ConfigClient:
    """Client for the Vantage Application Communication Interface (ACI) service.

    This client handles connecting to the ACI service, authenticating, and the
    serialization/deserialization of XML requests and responses.
    """

    def __init__(
        self,
        host: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        *,
        use_ssl: Union[ssl.SSLContext, bool] = True,
        port: Optional[int] = None,
        conn_timeout: float = 5,
        read_timeout: float = 60,
    ):
        """Initialize the ConfigClient instance.

        Args:
            host: The hostname or IP address of the ACI service.
            username: The username to use when authenticating with the ACI service.
            password: The password to use when authenticating with the ACI service.
            use_ssl: Whether to use SSL when connecting to the ACI service.
            port: The port to use when connecting to the ACI service.
            conn_timeout: The timeout to use when connecting.
            read_timeout: The timeout to use when making requests.
        """

        self._host = host
        self._username = username
        self._password = password
        self._ssl_context = None
        self._logger = logging.getLogger(__name__)
        self._connection: Optional[Connection] = None
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout
        self._lock = asyncio.Lock()

        # Set up SSL context
        if use_ssl is True:
            # We don't have a local issuer certificate to check against, and we'll be
            # connecting to an IP address so we can't check the hostname
            self._ssl_context = ssl.create_default_context()
            self._ssl_context.check_hostname = False
            self._ssl_context.verify_mode = ssl.CERT_NONE
        elif isinstance(use_ssl, ssl.SSLContext):
            self._ssl_context = use_ssl

        # Set up port
        if port is None:
            self._port = 2010 if use_ssl else 2001
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
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Exit context manager."""
        self.close()
        if exc_val:
            raise exc_val

    def close(self) -> None:
        """Close any open connections to the ACI service."""

        # Check if connection is already closed
        if self._connection is None or self._connection[1].is_closing():
            return

        # Close the connection
        _, writer = self._connection
        writer.close()

        self._logger.debug("Connection closed")

    async def raw_request(self, interface: str, payload: str) -> str:
        """Send a plaintext request to the ACI service.

        Args:
            interface: The interface to send the request to
            payload: The request payload string to send

        Returns:
            The response payload string
        """

        async with self._lock:
            # Get a connection
            reader, writer = await self._get_connection()

            try:
                # Send the request
                request = f"<{interface}>{payload}</{interface}>"
                writer.write(request.encode())
                await writer.drain()

                # Fetch the response
                end_bytes = f"</{interface}>\n".encode()
                data = await asyncio.wait_for(
                    reader.readuntil(end_bytes), timeout=self._read_timeout
                )

            except asyncio.TimeoutError as err:
                raise ClientTimeoutError from err
            except (OSError, asyncio.IncompleteReadError) as err:
                raise ClientConnectionError from err

            return data.decode()

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
        self._logger.debug(request)

        response = await self.raw_request(method.interface, request)
        self._logger.debug(response)

        # Parse the XML doc
        tree = ET.fromstring(response)

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
                f"did not contain a return value"
            )

        return method.return_value

    async def _get_connection(self) -> Connection:
        """Get a connection to the ACI service, authenticating if necessary."""

        # If we already have a connection, return it
        if self._connection is not None and not self._connection[1].is_closing():
            return self._connection

        try:
            # Otherwise, open a new connection
            connection = await asyncio.wait_for(
                asyncio.open_connection(
                    self._host,
                    self._port,
                    ssl=self._ssl_context,
                    limit=2**20,
                ),
                timeout=self._conn_timeout,
            )
            self._connection = connection
            self._logger.info("Connected")

            # Login if we have a username and password
            await self._login()

        except asyncio.TimeoutError as err:
            raise ClientTimeoutError from err
        except OSError as err:
            raise ClientConnectionError from err

        return connection

    async def _login(self) -> None:
        # Authenticate if necessary

        if self._username is None or self._password is None:
            return

        params = Login.Params(user=self._username, password=self._password)
        success = await self.request(Login, params)
        if not success:
            raise PermissionError("Authentication failed, bad username or password")

        self._logger.info("Login successful")
