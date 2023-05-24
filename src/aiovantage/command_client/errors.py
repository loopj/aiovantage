import asyncio


class ClientError(Exception):
    pass


class ClientConnectionError(ClientError):
    pass


class ClientTimeoutError(asyncio.TimeoutError, ClientConnectionError):
    pass


class CommandError(ClientError):
    @classmethod
    def from_string(cls, message: str) -> "CommandError":
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
    pass


class LoginFailedError(CommandError):
    pass
