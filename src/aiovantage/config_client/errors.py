"""Config client exceptions."""

import asyncio


class ClientError(Exception):
    """Base exception for config client."""


class ClientConnectionError(ClientError):
    """Exception for config client connection errors."""


class ClientTimeoutError(asyncio.TimeoutError, ClientConnectionError):
    """Exception for command client connection errors caused by timeouts."""


class LoginFailedError(ClientError):
    """Login failed."""
