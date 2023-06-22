"""Client exceptions."""

import asyncio


class ClientError(Exception):
    """Base exception for config client."""


class ClientConnectionError(ClientError):
    """Exception for config client connection errors."""


class ClientTimeoutError(asyncio.TimeoutError, ClientConnectionError):
    """Exception for command client connection errors caused by timeouts."""


class CommandError(ClientError):
    """Base exception for errors returned by the Host Command service."""


class LoginFailedError(CommandError):
    """Login failed."""


class LoginRequiredError(CommandError):
    """Login is required to perform this command."""
