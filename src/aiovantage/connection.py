"""Wrapper for an asyncio connection to a Vantage controller."""

import asyncio
from ssl import CERT_NONE, SSLContext, create_default_context
from typing import ClassVar, Optional, Union

from .errors import ClientConnectionError, ClientTimeoutError


class BaseConnection:
    """Wrapper for an asyncio connection to a Vantage controller."""

    default_port: ClassVar[int]
    default_ssl_port: ClassVar[int]
    buffer_limit: ClassVar[int] = 2**16

    def __init__(
        self,
        host: str,
        port: Optional[int] = None,
        ssl: Union[SSLContext, bool] = True,
        conn_timeout: Optional[float] = None,
    ) -> None:
        """Initialize the connection."""
        self._host = host
        self._conn_timeout = conn_timeout
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None

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
            self._port = self.default_ssl_port if ssl else self.default_port
        else:
            self._port = port

    async def open(self) -> None:
        """Open the connection."""
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
                    limit=self.buffer_limit,
                ),
                timeout=self._conn_timeout,
            )
        except asyncio.TimeoutError as exc:
            raise ClientTimeoutError(
                f"Timeout connecting to {self._host}:{self._port}"
            ) from exc
        except OSError as exc:
            raise ClientConnectionError(
                f"Failed to connect to {self._host}:{self._port}"
            ) from exc

    def close(self) -> None:
        """Close the connection."""
        if self._writer is not None and not self._writer.is_closing():
            self._writer.close()
            self._writer = None

    @property
    def host(self) -> str:
        """Return the host."""
        return self._host

    @property
    def port(self) -> int:
        """Return the port."""
        return self._port

    @property
    def closed(self) -> bool:
        """Return whether the connection is closed."""
        return self._writer is None or self._writer.is_closing()

    async def write(self, message: str) -> None:
        """Send a plaintext message.

        Args:
            message: The message to send, as a string.
        """
        # Make sure we're connected
        if self._writer is None or self._writer.is_closing():
            raise ClientConnectionError("Client not connected.")

        # Send the request
        try:
            self._writer.write(message.encode())
            await self._writer.drain()
        except OSError as err:
            raise ClientConnectionError from err

    async def readuntil(self, separator: bytes, timeout: Optional[float] = None) -> str:
        """Read data until the separator is found or the optional timeout is reached.

        Args:
            separator: The separator to read until.
            timeout: The optional timeout in seconds.

        Returns:
            The data read, as a string.
        """
        # Make sure we're connected
        if self._reader is None or self.closed:
            raise ClientConnectionError("Client not connected.")

        # Read the response, with optional timeout
        try:
            data = await asyncio.wait_for(self._reader.readuntil(separator), timeout)
        except (OSError, asyncio.IncompleteReadError) as err:
            raise ClientConnectionError from err
        except asyncio.TimeoutError as err:
            raise ClientTimeoutError from err

        return data.decode()
