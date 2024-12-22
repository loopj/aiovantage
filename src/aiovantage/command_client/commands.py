"""Send commands to the Vantage Host Command service."""

import asyncio
import logging
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from ssl import SSLContext
from types import TracebackType

from typing_extensions import Self

from aiovantage.connection import BaseConnection
from aiovantage.errors import (
    CommandError,
    InvalidObjectError,
    LoginFailedError,
    LoginRequiredError,
)

from .utils import encode_params, tokenize_response


class CommandConnection(BaseConnection):
    """Connection to a Vantage Host Command service."""

    default_port = 3001
    default_ssl_port = 3010


@dataclass
class CommandResponse:
    """Wrapper for command responses."""

    command: str
    args: Sequence[str]
    data: Sequence[str]


class CommandClient:
    """Client to send commands to the Vantage Host Command service."""

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
        self._connection = CommandConnection(
            host, port, ssl=ssl, conn_timeout=conn_timeout
        )
        self._username = username
        self._password = password
        self._read_timeout = read_timeout
        self._connection_lock = asyncio.Lock()
        self._command_lock = asyncio.Lock()
        self._logger = logging.getLogger(__name__)

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
        """Close the connection to the Host Command service."""
        self._connection.close()

    async def command(
        self,
        command: str,
        *params: str | float | Decimal,
        force_quotes: bool = False,
        connection: CommandConnection | None = None,
    ) -> CommandResponse:
        """Send a command to the Host Command service and wait for a response.

        Args:
            command: The command to send, should be a single word string.
            params: The parameters to send with the command.
            force_quotes: Whether to force string params to be wrapped in double quotes.
            connection: The connection to use, if not the default.

        Returns:
            A CommandResponse instance.
        """
        # Build the request
        request = command
        if params:
            request += f" {encode_params(*params, force_quotes=force_quotes)}"

        # Send the request and parse the response
        *data, return_line = await self.raw_request(request, connection=connection)
        command, *args = tokenize_response(return_line)
        return CommandResponse(command[2:], args, data)

    async def raw_request(
        self, request: str, connection: CommandConnection | None = None
    ) -> Sequence[str]:
        """Send a raw command to the Host Command service and return all response lines.

        Handles authentication if required, and raises an exception if the response line
        contains R:ERROR.

        Args:
            request: The request to send.
            connection: The connection to use, if not the default.

        Returns:
            The response lines received from the server.
        """
        conn = connection or await self.get_connection()

        # Send the command
        async with self._command_lock:
            self._logger.debug("Sending command: %s", request)
            await conn.write(f"{request}\n")

            # Read all lines of the response
            response_lines = []
            while True:
                response_line = await conn.readuntil(b"\r\n", self._read_timeout)
                response_line = response_line.rstrip()

                # Handle error codes
                if response_line.startswith("R:ERROR"):
                    raise self._parse_command_error(response_line)

                # Ignore potentially interleaved "event" messages
                if any(response_line.startswith(x) for x in ("S:", "L:", "EL:")):
                    self._logger.debug("Ignoring event message: %s", response_line)
                    continue

                # Return the response once we see the response line
                response_lines.append(response_line)
                if response_line.startswith("R:"):
                    break

        self._logger.debug("Received response: %s", "\n".join(response_lines))

        return response_lines

    async def get_connection(self) -> CommandConnection:
        """Get a connection to the Host Command service."""
        async with self._connection_lock:
            if self._connection.closed:
                # Open a new connection
                await self._connection.open()

                # Authenticate the new connection if we have credentials
                if self._username and self._password:
                    await self.command(
                        "LOGIN",
                        self._username,
                        self._password,
                        connection=self._connection,
                    )

                self._logger.info(
                    "Connected to command client at %s:%d",
                    self._connection.host,
                    self._connection.port,
                )

            return self._connection

    def _parse_command_error(self, message: str) -> CommandError:
        # Parse a command error from a message.
        tag, error_message = message.split(" ", 1)
        _, _, error_code_str = tag.split(":")
        error_code = int(error_code_str)

        exc: CommandError
        if error_code == 7:
            exc = InvalidObjectError(error_message)
        elif error_code == 21:
            exc = LoginRequiredError(error_message)
        elif error_code == 23:
            exc = LoginFailedError(error_message)
        else:
            exc = CommandError(f"{error_message} (Error code {error_code})")

        return exc
