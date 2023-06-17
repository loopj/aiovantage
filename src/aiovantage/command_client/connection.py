"""A connection to the Vantage Host Command service."""

import asyncio
from decimal import Decimal
import logging
from ssl import SSLContext
from types import TracebackType
from typing import AsyncIterator, List, Optional, Set, Type, Union

from typing_extensions import Self

from .errors import ClientConnectionError, ClientTimeoutError, CommandError
from .response import CommandResponse
from .utils import create_ssl_context, encode_params


class CommandConnection:
    """A connection to the Vantage Host Command service."""

    def __init__(
        self,
        host: str,
        port: Optional[int] = None,
        *,
        ssl: Union[SSLContext, bool] = True,
        conn_timeout: Optional[float] = 5,
        read_timeout: Optional[float] = 10,
    ) -> None:
        """Create a connection to the Vantage Host Command service.

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

        self._delimiter = b"\r\n"
        self._command_lock: asyncio.Lock = asyncio.Lock()
        self._response_buffer: List[str] = []
        self._response_queue: asyncio.Queue[
            Union[CommandResponse, Exception]
        ] = asyncio.Queue(1)
        self._event_queues: Set[asyncio.Queue[Union[str, Exception]]] = set()
        self._task: Optional[asyncio.Task[None]] = None
        self._logger = logging.getLogger(__name__)

        # Set up the SSL context
        self._ssl: Optional[SSLContext]
        if ssl is True:
            self._ssl = create_ssl_context()
        elif isinstance(ssl, SSLContext):
            self._ssl = ssl
        else:
            self._ssl = None

        # Set up the port
        self._port: int
        if port is None:
            self._port = 3010 if ssl else 3001
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
        """Open a connection to the Vantage Host Command service."""

        # If we're already connected, do nothing
        if self._writer is not None and not self._writer.is_closing():
            return

        # Create the connection
        try:
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self._host, self._port, ssl=self._ssl),
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

        # Start the message handler task
        self._task = asyncio.create_task(self._message_handler())

    def close(self) -> None:
        """Close the connection to the Vantage Host Command service."""

        # Cancel the message handler task
        if self._task is not None:
            self._task.cancel()
            self._task = None

        # Close the underlying connection
        if self._writer is not None and not self._writer.is_closing():
            self._writer.close()
            self._writer = None

    @property
    def closed(self) -> bool:
        """Whether the connection is closed."""

        return self._writer is None or self._writer.is_closing()

    async def command(
        self,
        command: str,
        *params: Union[str, int, float, Decimal, bool],
        force_quotes: bool = False,
    ) -> CommandResponse:
        """Send a command to the Host Command service and wait for a response.

        Handles encoding the parameters correctly, and raises an exception if the
        response line is R:ERROR.

        Args:
            command: The command to send, should be a single word string.
            params: The parameters to send with the command.
            force_quotes: Whether to force string params to be wrapped in double quotes.

        Returns:
            A CommandResponse instance.
        """

        # Make sure we're connected
        if self._writer is None or self._writer.is_closing():
            raise ClientConnectionError("Not connected to Vantage Host Command service")

        # Build the request string, encoding the parameters if necessary
        if params:
            request = f"{command} {encode_params(*params, force_quotes=force_quotes)}"
        else:
            request = command

        # Send the request and wait for the response as a single transaction
        async with self._command_lock:
            # Send the request
            try:
                self._logger.debug("Sending command: %s", request)
                self._writer.write(f"{request}\n".encode())
                await self._writer.drain()
            except OSError as exc:
                raise ClientConnectionError("Connection error") from exc

            # Wait for the response
            try:
                response = await asyncio.wait_for(
                    self._response_queue.get(), timeout=self._read_timeout
                )
                self._logger.debug("Received response: %s", response)
            except asyncio.TimeoutError as exc:
                raise ClientTimeoutError("Timeout waiting for response") from exc

        # Re-raise connection errors, EOF, etc. as a connection error
        if isinstance(response, (OSError, asyncio.IncompleteReadError)):
            raise ClientConnectionError("Connection error") from response

        # Re-raise all other exceptions, including "R:ERROR" responses
        if isinstance(response, Exception):
            raise response

        return response

    async def events(self) -> AsyncIterator[str]:
        """Yield events from the Host Command service.

        Yields:
            "S:" (Status) or "EL:" (Event Log) strings from the Host Command service.
        """

        queue: asyncio.Queue[Union[str, Exception]] = asyncio.Queue(1024)
        try:
            self._event_queues.add(queue)

            while True:
                event = await queue.get()

                # Re-raise connection errors, EOF, etc. as a connection error
                if isinstance(event, (OSError, asyncio.IncompleteReadError)):
                    raise ClientConnectionError("Connection error") from event

                # Re-raise all other exceptions
                if isinstance(event, Exception):
                    raise event

                yield event
        finally:
            self._event_queues.remove(queue)

    async def _message_handler(self) -> None:
        # Task to handle potentially interleaved incoming messages from the Host Command
        # service and send them to the appropriate queues.

        assert self._reader is not None

        while True:
            try:
                line = await self._reader.readuntil(self._delimiter)
                message = line.decode().rstrip()
                if message.startswith("R:ERROR"):
                    self._put_response(CommandError.from_string(message))
                    self._response_buffer = []
                elif message.startswith("R:"):
                    self._response_buffer.append(message)
                    self._put_response(CommandResponse(self._response_buffer))
                    self._response_buffer = []
                elif message.startswith("S:") or message.startswith("EL:"):
                    self._put_event(message)
                else:
                    self._response_buffer.append(message)
            except Exception as exc:
                self._put_response(exc, warn=False)
                self._put_event(exc)
                break

        # Explicitly close the connection
        if self._writer is not None and not self._writer.is_closing():
            self._writer.close()
            self._writer = None

    def _put_event(self, event: Union[str, Exception]) -> None:
        # Send an event to all event queues.

        for queue in self._event_queues:
            if queue.full():
                dropped_event = queue.get_nowait()
                self._logger.warning(
                    "Event queue full trying to put '%s', "
                    "dropping oldest event '%s' to make room.",
                    event,
                    dropped_event,
                )

            queue.put_nowait(event)

    def _put_response(
        self, response: Union[CommandResponse, Exception], warn: bool = True
    ) -> None:
        # Send a response to the response queue, discard if no command is waiting.

        if self._command_lock.locked():
            if not self._response_queue.empty():
                old_response = self._response_queue.get_nowait()
                self._logger.error(
                    "Response queue not empty when trying to put '%s', "
                    "dropping previous response '%s'.",
                    response,
                    old_response,
                )

            self._response_queue.put_nowait(response)
        elif warn:
            self._logger.error(
                "Discarding response message, no command waiting: %s", response
            )
