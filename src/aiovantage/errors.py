"""Client exceptions."""

import asyncio


class ClientError(Exception):
    """Base exception for clients."""


class ClientConnectionError(ClientError):
    """Exception for client connection errors."""


class ClientTimeoutError(asyncio.TimeoutError, ClientConnectionError):
    """Exception for client connection errors caused by timeouts."""


class ClientResponseError(ClientError):
    """Exception for client response errors."""


class CommandError(ClientError):
    """Base exception for errors caused by sending commands or requests."""


class LoginFailedError(CommandError):
    """Login failed."""


class LoginRequiredError(CommandError):
    """Login is required to perform this command."""


class InvalidObjectError(CommandError):
    """The requested object ID is invalid."""


class ObjectOfflineError(CommandError):
    """The requested object is offline."""


class NotImplementedError(CommandError):
    """The requested command is not implemented."""
