class NotConnectedError(Exception):
    pass


class CommandError(Exception):
    pass


class LoginRequiredError(CommandError):
    pass


class LoginFailedError(CommandError):
    pass


def command_error_from_string(message: str) -> CommandError:
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
