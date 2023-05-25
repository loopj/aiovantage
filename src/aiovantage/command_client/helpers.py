import re
from typing import Sequence


def tokenize_response(string: str) -> Sequence[str]:
    """
    Tokenize a response from the Host Command service, handling quoted strings and
    byte arrays (in curly braces) as single tokens.

    Args:
        string: The response string to tokenize.

    Returns:
        A list of string tokens.
    """

    return re.findall(r'("[^"]*"|\{[^}]*\}|\S+)', string)
