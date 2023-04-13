import asyncio
import logging
import ssl
from types import TracebackType
from typing import Any, Optional, Protocol, Tuple, Type, TypeVar, Union

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.utils.text import snake_case

from .interfaces import ILogin
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
    call: Optional[Any]
    return_value: Optional[T]


class ACIClient:
    """Communicate with a Vantage InFusion ACI service."""

    def __init__(
        self,
        host: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        *,
        use_ssl: Union[ssl.SSLContext, bool] = True,
        port: Optional[int] = None,
        conn_timeout: float = 5,
        request_timeout: float = 60,
    ):
        self._host = host
        self._username = username
        self._password = password
        self._ssl_context = None
        self._logger = logging.getLogger(__name__)
        self._connection: Optional[
            Tuple[asyncio.StreamReader, asyncio.StreamWriter]
        ] = None
        self._conn_timeout = conn_timeout
        self._request_timeout = request_timeout

        if use_ssl == True:
            self._ssl_context = _default_ssl_context()
        elif isinstance(ssl, ssl.SSLContext):
            self._ssl_context = ssl

        if port is None:
            self._port = 2010 if use_ssl else 2001
        else:
            self._port = port

        self._parser = XmlParser(config=ParserConfig(fail_on_unknown_properties=False))
        self._serializer = XmlSerializer(config=SerializerConfig(xml_declaration=False))

    async def __aenter__(self) -> "ACIClient":
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def connect(self) -> None:
        """Connect to the ACI service, and authenticate if necessary."""

        self._connection = await asyncio.wait_for(
            asyncio.open_connection(
                self._host,
                self._port,
                ssl=self._ssl_context,
            ),
            timeout=self._conn_timeout,
        )
        self._logger.debug("Connection opened")

        await self._login()

    async def close(self) -> None:
        """Close the connection to the ACI service."""

        if self._connection is None:
            return

        _, writer = self._connection
        writer.close()
        await writer.wait_closed()

        self._connection = None
        self._logger.debug("Connection closed")

    async def raw_request(self, request_payload: str, end_token: str) -> str:
        """Send a plaintext request to the ACI service"""

        if self._connection is None:
            raise RuntimeError("Not connected to the ACI service")

        # Send the request
        reader, writer = self._connection
        writer.write(request_payload.encode())
        await writer.drain()

        # Fetch the response
        buffer = bytearray()
        end_bytes = end_token.encode()
        while True:
            # Read a chunk of data from the socket
            chunk = await asyncio.wait_for(
                reader.read(1024),
                timeout=self._request_timeout,
            )

            # Check for no data
            if not chunk:
                break

            # Check for a closed connection
            if chunk == b"\x18":
                raise EOFError(
                    "Connection closed by remote host, likely due to malformed request."
                )

            # Add chunk to buffer and check for end token
            buffer.extend(chunk)
            if end_bytes in buffer:
                break

        return buffer.decode()

    async def request(
        self,
        interface: Type[Any],
        method: Type[Method[T]],
        params: Any = None,
    ) -> T:
        """Marshall a request, send it to the ACI service, and yield a parsed object."""

        request = self._marshall(interface, method, params)
        self._logger.debug(request)

        response = await self.raw_request(request, f"</{interface.__name__}>")
        self._logger.debug(response)

        return self._unmarshall(interface, method, response)

    def _marshall(
        self,
        interface_cls: Type[Any],
        method_cls: Type[Method[T]],
        params: Any,
    ) -> str:
        method = method_cls()
        method.call = params

        interface = interface_cls()
        setattr(interface, snake_case(method_cls.__name__), method)

        return self._serializer.render(interface)

    def _unmarshall(
        self,
        interface_cls: Type[Any],
        method_cls: Type[Method[T]],
        response_str: str,
    ) -> T:
        interface = self._parser.from_string(response_str, interface_cls)
        method: Method[T] = getattr(interface, snake_case(method_cls.__name__))

        if method.return_value is None:
            raise TypeError(
                f"Response from {interface_cls.__name__}.{method_cls.__name__} did not contain a return value"
            )

        return method.return_value

    async def _login(self) -> None:
        if self._username is None or self._password is None:
            return

        params = Login.Params(user=self._username, password=self._password)
        success = await self.request(ILogin, Login, params)
        if not success:
            raise PermissionError("Authentication failed, bad username or password")

        self._logger.debug("Login successful")
