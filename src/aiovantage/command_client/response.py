"""Simple wrapper for command responses from the Vantage Host Command service."""

from dataclasses import dataclass
from typing import List

from .utils import tokenize_response


@dataclass
class CommandResponse:
    """Simple wrapper for command responses from the Vantage Host Command service."""

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
