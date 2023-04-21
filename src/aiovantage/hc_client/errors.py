class CommandExecutionError(Exception):
    pass


class LoginRequiredError(CommandExecutionError):
    pass


class LoginFailedError(CommandExecutionError):
    pass
