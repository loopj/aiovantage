"""Send commands to the Vantage Host Command service."""

import asyncio
import logging
from dataclasses import dataclass
from decimal import Decimal
from ssl import SSLContext
from types import TracebackType
from typing import List, Optional, Type, Union

from typing_extensions import Self

from aiovantage.connection import BaseConnection
from aiovantage.errors import CommandError, LoginFailedError, LoginRequiredError

from .utils import encode_params, tokenize_response


class CommandConnection(BaseConnection):
    """Connection to a Vantage Host Command service."""

    default_port = 3001
    default_ssl_port = 3010


@dataclass
class CommandResponse:
    """Wrapper for command responses from the Vantage Host Command service."""

    command: str
    """The command that was sent."""

    args: List[str]
    """The arguments of the "R:" line of the response."""

    data: List[str]
    """The data lines of the response, before the "R:" line."""

    def __init__(self, data: List[str]) -> None:
        """Initialize a CommandResponse."""
        # Extract "data" lines from the response. These are any lines before the
        # "R:" line, from commands such as "HELP" and "LISTSTATUS".
        self.data, return_line = data[:-1], data[-1]

        # Split the "R:" line into the command and arguments
        command, *self.args = tokenize_response(return_line)

        # Remove the "R:" prefix from the command
        self.command = command[2:]


class CommandClient:
    """Client to send commands to the Vantage Host Command service."""

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
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        traceback: Optional[TracebackType],
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
        *params: Union[str, int, float, Decimal],
        force_quotes: bool = False,
        connection: Optional[CommandConnection] = None,
    ) -> CommandResponse:
        """Send a command to the Host Command service and wait for a response.

        Handles encoding the parameters correctly, and raises an exception if the
        response line is R:ERROR.

        Args:
            command: The command to send, should be a single word string.
            params: The parameters to send with the command.
            force_quotes: Whether to force string params to be wrapped in double quotes.
            connection: The connection to use, if not the default.

        Returns:
            A CommandResponse instance.
        """
        # Get a connection to the Host Command service
        conn = connection or await self.get_connection()

        # Build the request string, encoding the parameters if necessary
        if params:
            request = f"{command} {encode_params(*params, force_quotes=force_quotes)}"
        else:
            request = command

        # Send the command
        async with self._command_lock:
            self._logger.debug("Sending command: %s", request)
            await conn.write(f"{request}\n")

            # Read the response
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

        response = CommandResponse(response_lines)
        self._logger.debug("Received response: %s", response)

        return response

    async def get_connection(self) -> CommandConnection:
        """Get a connection to the Host Command service."""
        async with self._connection_lock:
            if self._connection.closed:
                # Open a new connection
                await self._connection.open()

                # Authenticate the new connection if we have credentials
                if self._username is not None and self._password is not None:
                    await self.command(
                        "LOGIN",
                        self._username,
                        self._password,
                        connection=self._connection,
                    )

            return self._connection

    def _parse_command_error(self, message: str) -> CommandError:
        # Parse a command error from a message.
        tag, error_message = message.split(" ", 1)
        _, _, error_code_str = tag.split(":")
        error_code = int(error_code_str)

        exc: CommandError
        if error_code == 21:
            exc = LoginRequiredError(error_message)
        elif error_code == 23:
            exc = LoginFailedError(error_message)
        else:
            exc = CommandError(f"{error_message} (Error code {error_code})")

        return exc
