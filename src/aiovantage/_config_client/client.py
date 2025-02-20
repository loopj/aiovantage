import asyncio
import datetime as dt
from collections.abc import Callable
from ssl import SSLContext
from types import TracebackType
from typing import Any, Protocol, TypeVar

from typing_extensions import Self, override
from xsdata.formats.converter import BoolConverter, DateTimeConverter, converter
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

Interface = TypeVar("Interface")
Call = TypeVar("Call")
Return = TypeVar("Return")


class Method(Protocol[Call, Return]):
    """Method protocol."""

    call: Call | None
    result: Return | None


class ConfigClient:
    """Client for the Vantage Application Communication Interface (ACI) service.

    Connections are created lazily when needed, and closed when the client is closed.

    Args:
        host: The hostname or IP address of the Vantage controller.
        username: The username to use for authentication.
        password: The password to use for authentication.
        ssl: The SSL context to use. True will use a default context, False will disable SSL.
        ssl_context_factory: A factory function to use when creating default SSL contexts.
        port: The port to connect to.
        conn_timeout: The connection timeout in seconds.
        read_timeout: The read timeout in seconds.
    """

    def __init__(
        self,
        host: str,
        username: str | None = None,
        password: str | None = None,
        *,
        ssl: SSLContext | bool = True,
        ssl_context_factory: Callable[[], SSLContext] | None = None,
        port: int | None = None,
        conn_timeout: float = 30,
        read_timeout: float = 60,
    ) -> None:
        """Initialize the client."""
        self._connection = ConfigConnection(
            host,
            port=port,
            ssl=ssl,
            ssl_context_factory=ssl_context_factory,
            conn_timeout=conn_timeout,
        )

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

    async def raw_request(self, request: str, separator: str) -> str:
        """Send a raw XML request to the ACI service and return the raw XML response.

        Args:
            request: The raw XML request to send.
            separator: Read data from the stream until `separator` is found.

        Returns:
            The raw XML response.
        """
        # Open the connection if it's closed
        conn = await self._get_connection()

        # Send the request and read the response
        logger.debug("Sending request: %s", request)
        async with self._request_lock:
            await conn.write(request)
            response = await conn.readuntil(separator.encode(), self._read_timeout)

        logger.debug("Received response: %s", response)

        return response

    async def rpc(
        self,
        interface_cls: type[Interface],
        method_cls: type[Method[Call, Return]],
        params: Call | None = None,
    ) -> Return:
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
        method_attr = snake_case(method_cls.__name__)

        # Build an interface instance with the method
        request = interface_cls(**{method_attr: method})

        # Build the request
        request_str = self._serializer.render(request)  # type: ignore
        response_str = await self.raw_request(
            request_str, f"</{type(request).__name__}>\n"
        )

        # Parse the response
        response = self._parser.from_string(response_str, type(request))

        # Extract the method response
        method_response: Method[Call, Return] | None = getattr(
            response, method_attr, None
        )

        # Validate the response
        if (
            not isinstance(method_response, method_cls)
            or method_response.result is None
        ):
            raise ClientResponseError("Failed to parse response")

        return method_response.result

    def close(self) -> None:
        """Close the connection to the ACI service."""
        self._connection.close()

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


def _pascal_case_preserve(name: str) -> str:
    # Convert a field/class name to PascalCase, preserving existing PascalCase names.
    # This is helpful for class names like IConfiguration, etc. which get clobbered by
    # the default pascal_case function.
    if "_" in name or name.islower():
        return pascal_case(name)
    else:
        return name


# Vantage ACI service DateTime converter.
# Truncates microseconds and sets the timezone to UTC, to ensure consistency with
# datetimes from the HC service.
class _DateTimeConverter(DateTimeConverter):
    @override
    def deserialize(self, value: Any, **kwargs: Any) -> dt.datetime:
        out = super().deserialize(value, **kwargs)
        return out.replace(microsecond=0, tzinfo=dt.timezone.utc)


# Vantage ACI service bool converter.
# Adds support for mixed-case boolean values, in addition to standard xs:boolean values.
# This is required for attributes like "ExcludeFromWidgets" which have values like
# "True" and "False".
class _BoolConverter(BoolConverter):
    @override
    def deserialize(self, value: Any, **kwargs: Any) -> bool:
        if isinstance(value, str):
            value = value.lower()

        return super().deserialize(value, **kwargs)


# Register custom converters
converter.register_converter(dt.datetime, _DateTimeConverter())  # type: ignore
converter.register_converter(bool, _BoolConverter())  # type: ignore
