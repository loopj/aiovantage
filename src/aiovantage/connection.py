"""Base async TCP connection class."""

import asyncio
from ssl import CERT_NONE, SSLContext, create_default_context
from types import TracebackType
from typing import ClassVar, Optional, Type, Union

from typing_extensions import Self

from .errors import ClientConnectionError, ClientTimeoutError


class BaseConnection:
    """Base async TCP connection class."""

    default_port: ClassVar[int]
    default_ssl_port: ClassVar[int]
    default_conn_timeout: ClassVar[float]
    default_read_timeout: ClassVar[float]
    buffer_limit: ClassVar[int] = 2**16

    def __init__(
        self,
        host: str,
        port: Optional[int] = None,
        ssl: Union[SSLContext, bool] = True,
        conn_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None,
    ) -> None:
        """Initialize the connection."""
        self._host = host
        self._conn_timeout = conn_timeout or self.default_conn_timeout
        self._read_timeout = read_timeout or self.default_read_timeout
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._lock = asyncio.Lock()

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
        """Open a connection."""

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
                f"Timout connecting to {self._host}:{self._port}"
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

    async def write(self, request: str) -> None:
        """Send a plaintext message."""

        # Make sure we're connected
        if self._writer is None or self._writer.is_closing():
            raise ClientConnectionError("Client not connected.")

        try:
            # Send the request
            self._writer.write(request.encode())
            await self._writer.drain()

        except OSError as err:
            raise ClientConnectionError from err

    async def readuntil(self, end_token: str = "\n") -> str:
        """Read a plaintext message."""

        # Make sure we're connected
        if self._reader is None or self.closed:
            raise ClientConnectionError("Client not connected.")

        try:
            # Read the response
            data = await self._reader.readuntil(end_token.encode())

        except (OSError, asyncio.IncompleteReadError) as err:
            raise ClientConnectionError from err

        return data.decode()

    async def readuntil_with_timeout(self, end_token: str = "\n") -> str:
        """Read a plaintext message, with a timeout."""

        try:
            data = await asyncio.wait_for(self.readuntil(end_token), self._read_timeout)
        except asyncio.TimeoutError as err:
            raise ClientTimeoutError from err

        return data
