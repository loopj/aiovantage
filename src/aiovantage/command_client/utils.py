"""Utility functions for the Host Command service client."""

import re
import struct
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


def parse_byte_string(byte_string: str) -> bytearray:
    """Convert a "bytes" parameter string to a byte array.

    "Bytes" parameters are sent as a string of signed 32-bit integers,
    separated by commas, and wrapped in curly braces.

    Args:
        byte_string: The byte array parameter, as a string.

    Returns:
        The byte array.
    """
    # Remove the curly braces, and split the string into tokens
    tokens = byte_string.strip("{}").split(",")

    # Strip whitespace, and remove empty tokens
    tokens = [token.strip() for token in tokens if token.strip()]

    # Convert each token to a signed 32-bit integer and create a byte array
    byte_array = bytearray()
    for token in tokens:
        signed_int = struct.pack("i", int(token))
        byte_array.extend(signed_int)

    return byte_array


def encode_byte_string(byte_array: bytearray) -> str:
    """Convert a byte array to a "bytes" parameter string.

    Args:
        byte_array: The byte array to convert.

    Returns:
        The byte array parameter, as a string.
    """
    # Convert each signed 32-bit integer in the byte array to a string token
    tokens = []
    for byte in range(0, len(byte_array), 4):
        signed_int = struct.unpack("i", byte_array[byte : byte + 4])[0]
        tokens.append(str(signed_int))

    # Join the tokens with commas and wrap in curly braces
    data = "{" + ",".join(tokens) + "}"

    return data
