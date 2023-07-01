"""Utility functions for the Host Command service client."""

import re
from decimal import Decimal
from typing import Sequence, Union

TOKEN_PATTERN = re.compile(r'"([^""]*(?:""[^""]*)*)"|(\{.*?\})|(\S+)')


def tokenize_response(string: str) -> Sequence[str]:
    """Tokenize a response from the Host Command service.

    Handles quoted strings and byte arrays (in curly braces) as single tokens.

    Args:
        string: The response string to tokenize.

    Returns:
        A list of string tokens.
    """
    tokens = []
    for match in TOKEN_PATTERN.finditer(string):
        token = match.group(0)

        # Remove quotes from quoted strings, and unescape quotes
        if token.startswith('"') and token.endswith('"'):
            token = token[1:-1].replace('""', '"')

        tokens.append(token)

    return tokens


def encode_params(
    *params: Union[str, int, float, Decimal], force_quotes: bool = False
) -> str:
    """Encode a list of parameters for sending to the Host Command service.

    Converts all params to strings, wraps strings in double quotes, and escapes
    double quotes.

    Args:
        params: The parameters to encode.
        force_quotes: Whether to force string params to be wrapped in double quotes.

    Returns:
        The encoded parameters, joined by spaces.
    """
    encoded_params = []

    for value in params:
        if isinstance(value, str):
            if '"' in value or " " in value or force_quotes:
                value = value.replace('"', '""')
                encoded_params.append(f'"{value}"')
            else:
                encoded_params.append(value)
        elif isinstance(value, (int, float, Decimal)):
            encoded_params.append(str(value))
        else:
            raise TypeError(f"Invalid value type: {type(value)}")

    return " ".join(encoded_params)
