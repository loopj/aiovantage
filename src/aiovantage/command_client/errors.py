"""Command client exceptions."""

import asyncio


class ClientError(Exception):
    """Base exception for command client."""


class ClientConnectionError(ClientError):
    """Exception for command client connection errors."""


class ClientTimeoutError(asyncio.TimeoutError, ClientConnectionError):
    """Exception for command client connection errors caused by timeouts."""


class CommandError(ClientError):
    """Base exception for errors returned by the Host Command service."""

    @classmethod
    def from_string(cls, message: str) -> "CommandError":
        """Create a CommandError from a string returned by the Host Command service."""
        tag, error_message = message.split(" ", 1)
        _, _, error_code_str = tag.split(":")
        error_code = int(error_code_str)

        exc: Exception
        if error_code == 21:
            exc = LoginRequiredError(error_message)
        elif error_code == 23:
            exc = LoginFailedError(error_message)
        else:
            exc = CommandError(f"{error_message} (Error code {error_code})")
        return exc


class LoginRequiredError(CommandError):
    """Login is required to perform this command."""


class LoginFailedError(CommandError):
    """Login failed."""
