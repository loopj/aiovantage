"""Client for sending commands to the Vantage Host Command service."""

import asyncio
import logging
import re
from dataclasses import dataclass
from ssl import SSLContext
from types import TracebackType
from typing import Any

from typing_extensions import Self

from aiovantage.errors import CommandError, raise_command_error

from .connection import CommandConnection
from .converter import serialize, tokenize


@dataclass
class CommandResponse:
    """Wrapper for command responses."""

    command: str
    args: list[str]
    data: list[str]


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
        self._connection = CommandConnection(host, port, ssl, conn_timeout)
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

    async def command(self, command: str, *params: Any) -> CommandResponse:
        """Send a command to the Host Command service and wait for a response.

        Args:
            command: The command to send, should be a single word string.
            params: The parameters to send with the command.

        Returns:
            A CommandResponse instance.
        """
        # Build the request
        request = command
        if params:
            request += " " + " ".join(serialize(p) for p in params)

        # Send the request
        *data, return_line = await self.raw_request(request)

        # Break the response into tokens
        command, *args = tokenize(return_line)

        # Parse the response
        return CommandResponse(command[2:], args, data)

    async def raw_request(self, request: str) -> list[str]:
        """Send a raw command to the Host Command service and return all response lines.

        Handles authentication if required, and raises an exception if the response line
        contains R:ERROR.

        Args:
            request: The request to send.

        Returns:
            The response lines received from the server.
        """
        conn = await self._get_connection()

        # Send the command
        async with self._command_lock:
            self._logger.debug("Sending command: %s", request)
            await conn.write(f"{request}\n")

            # Read all lines of the response
            response_lines: list[str] = []
            while True:
                response_line = await conn.readuntil(b"\r\n", self._read_timeout)
                response_line = response_line.rstrip()

                # Handle command errors
                if response_line.startswith("R:ERROR"):
                    # Parse a command error from a message.
                    match = re.match(r"R:ERROR:(\d+) (.+)", response_line)
                    if not match:
                        raise CommandError(response_line)

                    # Convert the error code to a specific exception, if possible
                    raise_command_error(int(match.group(1)), match.group(2))

                # Ignore potentially interleaved "event" messages
                if response_line.startswith(("S:", "L:", "EL:")):
                    self._logger.debug("Ignoring event message: %s", response_line)
                    continue

                # Return the response once we see the response line
                response_lines.append(response_line)
                if response_line.startswith("R:"):
                    break

        self._logger.debug("Received response: %s", "\n".join(response_lines))

        return response_lines

    async def _get_connection(self) -> CommandConnection:
        """Get a connection to the Host Command service."""
        async with self._connection_lock:
            if self._connection.closed:
                # Open a new connection
                await self._connection.open()

                # Authenticate the new connection if we have credentials
                if self._username and self._password:
                    await self._connection.authenticate(self._username, self._password)

                self._logger.info(
                    "Connected to command client at %s:%d",
                    self._connection.host,
                    self._connection.port,
                )

            return self._connection
