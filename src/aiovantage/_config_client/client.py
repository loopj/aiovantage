"""Client for the Vantage Application Communication Interface (ACI) service."""

import asyncio
from ssl import SSLContext
from types import TracebackType
from typing import Any, Protocol, TypeVar

from typing_extensions import Self
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.parsers.handlers import XmlEventHandler
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.utils.text import pascal_case, snake_case

from aiovantage._logger import logger
from aiovantage.errors import ClientResponseError, LoginRequiredError

from .connection import ConfigConnection

T = TypeVar("T")
U = TypeVar("U")


class Method(Protocol[T, U]):
    """Method protocol."""

    call: T | None
    result: U | None


def _pascal_case_preserve(name: str) -> str:
    # Convert a field/class name to PascalCase, preserving existing PascalCase names.
    if "_" in name or name.islower():
        return pascal_case(name)
    else:
        return name


class ConfigClient:
    """Client for the Vantage Application Communication Interface (ACI) service.

    This client handles connecting to the ACI service, authenticating, and the
    serialization/deserialization of XML requests and responses.
    """

    def __init__(
        self,
        host: str,
        username: str | None = None,
        password: str | None = None,
        *,
        ssl: SSLContext | bool = True,
        port: int | None = None,
        conn_timeout: float = 30,
        read_timeout: float = 60,
    ) -> None:
        """Initialize the client."""
        self._connection = ConfigConnection(host, port, ssl, conn_timeout)
        self._username = username
        self._password = password
        self._read_timeout = read_timeout
        self._connection_lock = asyncio.Lock()
        self._request_lock = asyncio.Lock()

        # Default to pascal case for element and attribute names
        xml_context = XmlContext(
            element_name_generator=_pascal_case_preserve,
            attribute_name_generator=_pascal_case_preserve,
            models_package="aiovantage._objects",
        )

        # Configure the request serializer
        self._serializer = XmlSerializer(
            config=SerializerConfig(xml_declaration=False),
            context=xml_context,
        )

        # Configure the response parser
        self._parser = XmlParser(
            config=ParserConfig(fail_on_unknown_properties=False),
            context=xml_context,
            handler=XmlEventHandler,
        )

    async def __aenter__(self) -> Self:
        """Return context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit context manager."""
        self.close()
        if exc_val:
            raise exc_val

    def close(self) -> None:
        """Close the connection to the ACI service."""
        self._connection.close()

    async def raw_request(self, request: str, delimiter: str) -> str:
        """Send a raw request to the ACI service and return the raw response.

        Args:
            request: The raw XML request to send.
            delimiter: The delimiter to use when reading the response.

        Returns:
            The raw XML response.
        """
        # Open the connection if it's closed
        conn = await self._get_connection()

        # Send the request and read the response
        logger.debug("Sending request: %s", request)
        async with self._request_lock:
            await conn.write(request)
            response = await conn.readuntil(delimiter.encode(), self._read_timeout)

        logger.debug("Received response: %s", response)

        return response

    async def request(self, request: T) -> T:
        """Send a request to the ACI service and return the response."""
        # Build and send the request
        request_str = self._serializer.render(request)  # type: ignore
        response_str = await self.raw_request(
            request_str, f"</{type(request).__name__}>\n"
        )

        # Parse the response
        return self._parser.from_string(response_str, type(request))

    async def rpc_call(
        self,
        interface_cls: type[Any],
        method_cls: type[Method[T, U]],
        params: T | None = None,
    ) -> U:
        """Call a remote procedure on the ACI service.

        Args:
            interface_cls: The interface class.
            method_cls: The method class to call.
            params: The parameters to pass to the method.

        Returns:
            The result of the method call.
        """
        # Build a method instance with the given parameters
        method = method_cls()
        method.call = params

        # Build an interface instance with the method
        request = interface_cls(**{snake_case(method_cls.__name__): method})

        # Send the request
        response = await self.request(request)

        # Extract the method response
        method_response: Method[T, U] | None = getattr(
            response, snake_case(method_cls.__name__), None
        )

        # Validate the response
        if (
            not isinstance(method_response, method_cls)
            or method_response.result is None
        ):
            raise ClientResponseError("Failed to parse response")

        return method_response.result

    async def _get_connection(self) -> ConfigConnection:
        """Get a connection to the ACI service."""
        async with self._connection_lock:
            if self._connection.closed:
                # Open a new connection
                await self._connection.open()

                # Authenticate the new connection if we have credentials
                if self._username and self._password:
                    await self._connection.authenticate(self._username, self._password)
                elif self._connection.requires_authentication:
                    raise LoginRequiredError(
                        "Login required, but no credentials were provided"
                    )

                logger.info(
                    "Connected to config client at %s:%d",
                    self._connection.host,
                    self._connection.port,
                )

            return self._connection
