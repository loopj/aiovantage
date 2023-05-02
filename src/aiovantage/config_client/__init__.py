import asyncio
import logging
import ssl
import xml.etree.ElementTree as ET
from types import TracebackType
from typing import Any, ClassVar, Optional, Protocol, Tuple, Type, TypeVar, Union

from typing_extensions import Self
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.parsers.handlers import XmlEventHandler
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from .methods.login import Login


def _default_ssl_context() -> ssl.SSLContext:
    # We don't have a local issuer certificate to check against, and we'll be
    # connecting to an IP address so we can't check the hostname
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    return context


T = TypeVar("T")


class Method(Protocol[T]):
    interface: ClassVar[str]
    call: Optional[Any]
    return_value: Optional[T]


class ConfigClient:
    """
    Communicate with a Vantage InFusion ACI service.
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
        """
        Initialize the ConfigClient instance.

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
        self._connection: Optional[
            Tuple[asyncio.StreamReader, asyncio.StreamWriter]
        ] = None
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout

        if use_ssl is True:
            self._ssl_context = _default_ssl_context()
        elif isinstance(ssl, ssl.SSLContext):
            self._ssl_context = ssl

        if port is None:
            self._port = 2010 if use_ssl else 2001
        else:
            self._port = port

        self._parser = XmlParser(
            config=ParserConfig(fail_on_unknown_properties=False),
            handler=XmlEventHandler,
        )

        self._serializer = XmlSerializer(config=SerializerConfig(xml_declaration=False))

    async def __aenter__(self) -> Self:
        # Async context manager entry

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        # Async context manager exit

        await self.close()

    async def get_connection(self) -> Tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        """
        Get a connection to the ACI service, authenticating if necessary.
        """

        # If we already have a connection, return it
        if self._connection is not None and not self._connection[1].is_closing():
            return self._connection

        # Otherwise, open a new connection
        connection = await asyncio.wait_for(
            asyncio.open_connection(
                self._host,
                self._port,
                ssl=self._ssl_context,
            ),
            timeout=self._conn_timeout,
        )
        self._connection = connection
        self._logger.info("Connected")

        # Login if we have a username and password
        await self._login()

        return connection

    async def close(self) -> None:
        """
        Close any open connections to the ACI service.
        """

        # Check if connection is already closed
        if self._connection is None or self._connection[1].is_closing():
            return

        # Close the connection
        _, writer = self._connection
        writer.close()
        await writer.wait_closed()

        self._logger.debug("Connection closed")

    async def raw_request(self, request_payload: str, end_token: str) -> str:
        """
        Send a plaintext request to the ACI service.

        Args:
            request_payload: The request payload string to send
            end_token: The token to look for to indicate the end of the response

        Returns:
            The response payload string
        """

        # Get a connection
        reader, writer = await self.get_connection()

        # Send the request
        writer.write(request_payload.encode())
        await writer.drain()

        # Fetch the response
        end_bytes = end_token.encode()
        data = await reader.readuntil(end_bytes)

        return data.decode()

    async def request(self, method: Type[Method[T]], params: Any = None) -> T:
        """
        Marshall a request, send it to the ACI service, and yield a parsed object.

        Args:
            method: The method class to use
            params: The parameters instance to pass to the method

        Returns:
            The parsed response object
        """

        request = self._marshall(method, params)
        self._logger.debug(request)

        response = await self.raw_request(request, f"</{method.interface}>\n")
        self._logger.debug(response)

        return self._unmarshall(method, response)

    def _marshall(self, method_cls: Type[Method[T]], params: Any) -> str:
        # Serialize the request to XML using xsdata

        method = method_cls()
        method.call = params

        return (
            f"<{method.interface}>"
            f"{self._serializer.render(method)}"
            f"</{method.interface}>"
        )

    def _unmarshall(self, method_cls: Type[Method[T]], response_str: str) -> T:
        # Deserialize the response from XML using xsdata

        tree = ET.fromstring(response_str)
        method_el = tree.find(f"{method_cls.__name__}")
        method = self._parser.parse(method_el, method_cls)

        if method.return_value is None or method.return_value == "":
            raise TypeError(
                f"Response from {method_cls.interface}.{method_cls.__name__}"
                f"did not contain a return value"
            )

        return method.return_value

    async def _login(self) -> None:
        # Authenticate if necessary

        if self._username is None or self._password is None:
            return

        params = Login.Params(user=self._username, password=self._password)
        success = await self.request(Login, params)
        if not success:
            raise PermissionError("Authentication failed, bad username or password")

        self._logger.info("Login successful")
