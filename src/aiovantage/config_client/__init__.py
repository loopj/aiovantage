"""Client for the Vantage Application Communication Interface (ACI) service.

The ACI service is an XML-based RPC service that Design Center uses to communicate
with Vantage InFusion Controllers. There are a number of "interfaces" exposed, each
with one or more "methods".

This service allows you to query the "configuration" of a Vantage system, for
example fetching a list of all the objects, getting a backup of the Design Center
XML, etc.

The service is exposed on port 2010 (SSL) by default, and on port 2001 (non-SSL) if
this port has been opened by the firewall on the controller.

The service is discoverable via mDNS as `_aci._tcp.local` and/or
`_secure_aci._tcp.local`.
"""

import asyncio
import logging
from ssl import SSLContext
from types import TracebackType
from typing import Optional, Type, Union
from xml.etree import ElementTree

from typing_extensions import Self
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.parsers.handlers import XmlEventHandler
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from aiovantage.config_client.methods import Call, Method, Return
from aiovantage.config_client.methods.introspection import GetVersion
from aiovantage.config_client.methods.login import Login
from aiovantage.connection import BaseConnection
from aiovantage.errors import ClientResponseError, LoginFailedError, LoginRequiredError


class ConfigConnection(BaseConnection):
    """Connection to a Vantage ACI server."""

    default_port = 2001
    default_ssl_port = 2010
    buffer_limit = 2**20


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
        ssl: Union[SSLContext, bool] = True,
        port: Optional[int] = None,
        conn_timeout: float = 30,
        read_timeout: float = 60,
    ) -> None:
        """Initialize the client."""
        self._connection = ConfigConnection(host, port, ssl, conn_timeout)
        self._username = username
        self._password = password
        self._read_timeout = read_timeout

        self._serializer = XmlSerializer(
            config=SerializerConfig(xml_declaration=False),
        )

        self._parser = XmlParser(
            config=ParserConfig(fail_on_unknown_properties=False),
            handler=XmlEventHandler,
        )
        self._connection_lock = asyncio.Lock()
        self._request_lock = asyncio.Lock()
        self._logger = logging.getLogger(__name__)

    async def __aenter__(self) -> Self:
        """Return context manager."""
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

    def close(self) -> None:
        """Close the connection to the ACI service."""
        self._connection.close()

    async def request(
        self,
        method_cls: Type[Method[Call, Return]],
        params: Optional[Call] = None,
        connection: Optional[ConfigConnection] = None,
    ) -> Optional[Return]:
        """Marshall a request, send it to the ACI service, and return a parsed object.

        Args:
            method_cls: The request method class to use.
            params: The parameters to pass to the method.
            connection: The connection to use, if not the default.

        Returns:
            The parsed response object
        """
        # Open the connection if it's closed
        conn = connection or await self.get_connection()

        # Build the method object
        method = method_cls()
        method.call = params

        # Render the method object to XML with xsdata
        request = (
            f"<{method.interface}>"
            + self._serializer.render(method)
            + f"</{method.interface}>"
        )
        self._logger.debug(request)

        # Send the request and read the response
        async with self._request_lock:
            await conn.write(request)
            response = await conn.readuntil(
                f"</{method.interface}>\n".encode(), timeout=self._read_timeout
            )
        self._logger.debug(response)

        # Parse the XML doc
        root = ElementTree.fromstring(response)

        # Response root must match the tag of the request
        if root.tag != method.interface:
            raise ClientResponseError(
                f"Response '{root.tag}' does not match request '{method.interface}'"
            )

        # Responses must contain the method element and a return element
        method_el = root.find(f"./{method_cls.__name__}")
        return_el = root.find(f"./{method_cls.__name__}/return")
        if method_el is None or return_el is None:
            raise ClientResponseError("Response is missing method or return element")

        # Return None if the method has empty return element.
        # This can happen when the client is not logged in, or when the method returns
        # no results, eg. IConfiguration.GetFilterResults.
        if return_el.text is None and len(return_el) == 0:
            return None

        # Parse the method element with xsdata
        method = self._parser.parse(method_el, method_cls)
        if method.return_value is None:
            return None

        return method.return_value

    async def get_connection(self) -> ConfigConnection:
        """Get a connection to the ACI service."""
        async with self._connection_lock:
            if self._connection.closed:
                await self._connection.open()

                # Ensure the connection is authenticated, if required
                if self._username is not None and self._password is not None:
                    # Log in if we have credentials
                    success = await self.request(
                        Login,
                        Login.Params(self._username, self._password),
                        self._connection,
                    )

                    if not success:
                        raise LoginFailedError("Login failed, bad username or password")
                else:
                    # Check if login is required if we don't have credentials
                    version = await self.request(
                        GetVersion,
                        connection=self._connection,
                    )

                    if version is None:
                        raise LoginRequiredError(
                            "Login required, but no credentials were provided"
                        )

            return self._connection
