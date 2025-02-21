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


class InvalidParameterError(CommandError):
    """An invalid parameter was provided."""


class WrongNumberOfParametersError(CommandError):
    """The wrong number of parameters was provided."""


class SyntaxError(CommandError):
    """The command syntax is invalid."""


class InvalidObjectError(CommandError):
    """The requested object ID is invalid."""


class NotImplementedError(CommandError):
    """The requested command is not implemented."""


class FailedError(CommandError):
    """The requested command failed."""


class NotConfiguredError(CommandError):
    """The requested object is not configured."""


class NotInitializedError(CommandError):
    """The requested object is not initialized."""


class NotSupportedError(CommandError):
    """The requested command is not supported."""


class ObjectOfflineError(CommandError):
    """The requested object is offline."""


class LoginRequiredError(CommandError):
    """Login is required to perform this command."""


class LoginFailedError(CommandError):
    """Login failed."""


COMMAND_ERROR_CODES = {
    4: InvalidParameterError,
    5: WrongNumberOfParametersError,
    6: SyntaxError,
    7: InvalidObjectError,
    8: NotImplementedError,
    12: FailedError,
    14: NotConfiguredError,
    16: NotInitializedError,
    17: NotSupportedError,
    20: ObjectOfflineError,
    21: LoginRequiredError,
    23: LoginFailedError,
}


def raise_command_error(code: int, message: str) -> None:
    """Raise a command error based on the error code."""
    error_cls = COMMAND_ERROR_CODES.get(code)

    if error_cls is None:
        raise CommandError(f"{message} (Error code {code})")

    raise error_cls(message)
