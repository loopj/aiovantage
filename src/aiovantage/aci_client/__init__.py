import asyncio
import logging
import ssl
from types import TracebackType
from typing import Any, Optional, Protocol, Type, TypeVar, Union

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.utils.text import snake_case

from .interfaces import ILogin, IIntrospection
from .methods.introspection import GetVersion
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
        request_timeout: float = 60,
    ):
        """
        Initialize the ACIClient instance.

        Args:
            host: The hostname or IP address of the ACI service.
            username: The username to use when authenticating with the ACI service.
            password: The password to use when authenticating with the ACI service.
            use_ssl: Whether to use SSL when connecting to the ACI service.
            port: The port to use when connecting to the ACI service.
            conn_timeout: The timeout to use when connecting
            request_timeout: The timeout to use when making requests
        """

        self._host = host
        self._username = username
        self._password = password
        self._ssl_context = None
        self._logger = logging.getLogger(__name__)
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._conn_timeout = conn_timeout
        self._request_timeout = request_timeout

        if use_ssl is True:
            self._ssl_context = _default_ssl_context()
        elif isinstance(ssl, ssl.SSLContext):
            self._ssl_context = ssl

        if port is None:
            self._port = 2010 if use_ssl else 2001
        else:
            self._port = port

        self._parser = XmlParser(config=ParserConfig(fail_on_unknown_properties=False))
        self._serializer = XmlSerializer(config=SerializerConfig(xml_declaration=False))

    async def connect(self) -> None:
        """
        Connect to the ACI service, and authenticate if necessary.
        """

        self._reader, self._writer = await asyncio.wait_for(
            asyncio.open_connection(
                self._host,
                self._port,
                ssl=self._ssl_context,
            ),
            timeout=self._conn_timeout,
        )
        self._logger.debug("Connection opened")

        await self._login()

    async def authenticated(self) -> bool:
        """Check if we are currently authenticated."""

        r = await self.request(IIntrospection, GetVersion)
        return r.app is not None

    async def close(self) -> None:
        """
        Close the connection to the ACI service.
        """

        if self._writer is None or self._writer.is_closing():
            return

        self._writer.close()
        await self._writer.wait_closed()

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

        # Connect if we're not already connected
        if self._writer is None or self._writer.is_closing():
            await self.connect()

        # Send the request
        self._writer.write(request_payload.encode()) # type: ignore[union-attr]
        await self._writer.drain() # type: ignore[union-attr]

        # Fetch the response
        end_bytes = end_token.encode()
        data = await self._reader.readuntil(end_bytes) # type: ignore[union-attr]

        return data.decode()

    async def request(
        self, interface: Type[Any], method: Type[Method[T]], params: Any = None
    ) -> T:
        """
        Marshall a request, send it to the ACI service, and yield a parsed object.

        Args:
            interface: The interface class to use
            method: The method class to use
            params: The parameters instance to pass to the method

        Returns:
            The parsed response object
        """

        request = self._marshall(interface, method, params)
        self._logger.debug(request)

        response = await self.raw_request(request, f"</{interface.__name__}>\n")
        self._logger.debug(response)

        return self._unmarshall(interface, method, response)

    async def __aenter__(self) -> "ACIClient":
        # Async context manager entry

        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        # Async context manager exit

        await self.close()

    def _marshall(
        self, interface_cls: Type[Any], method_cls: Type[Method[T]], params: Any
    ) -> str:
        # Serialize the request to XML using xsdata

        method = method_cls()
        method.call = params

        interface = interface_cls()
        setattr(interface, snake_case(method_cls.__name__), method)

        return self._serializer.render(interface)

    def _unmarshall(
        self, interface_cls: Type[Any], method_cls: Type[Method[T]], response_str: str
    ) -> T:
        # Deserialize the response from XML using xsdata

        interface = self._parser.from_string(response_str, interface_cls)
        method: Method[T] = getattr(interface, snake_case(method_cls.__name__))

        if method.return_value is None or method.return_value == "":
            raise TypeError(
                f"Response from {interface_cls.__name__}.{method_cls.__name__}"
                f"did not contain a return value"
            )

        return method.return_value

    async def _login(self) -> None:
        # Authenticate if necessary

        if self._username is None or self._password is None:
            return

        params = Login.Params(user=self._username, password=self._password)
        success = await self.request(ILogin, Login, params)
        if not success:
            raise PermissionError("Authentication failed, bad username or password")

        self._logger.debug("Login successful")
