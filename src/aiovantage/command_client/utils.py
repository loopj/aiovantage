"""Utility functions for the Host Command service client."""

import re
import struct
from decimal import Decimal, InvalidOperation
from typing import Any, Sequence, Type, Union

TOKEN_PATTERN = re.compile(r'"([^""]*(?:""[^""]*)*)"|(\{.*?\})|(\S+)')

ParameterType = Union[str, bool, int, float, Decimal, bytearray]


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


def parse_params(
    params: Sequence[str], signature: Sequence[Type[Any]]
) -> Sequence[ParameterType]:
    """Parse response parameters from the Host Command service.

    Handles parsing tokens into the expected types, as defined by the signature.

    Args:
        params: The parameters to parse.
        signature: The expected parameter types.

    Returns:
        A list of parameters of the correct type.

    Raises:
        ValueError: If the parameter count does not match the signature, if a
            parameter is of an unsupported type, or if a parameter cannot be parsed.
    """
    parsed_params = []
    for index, param in enumerate(params):
        if index >= len(signature):
            raise ValueError("More parameters than expected")

        parsed_param: ParameterType
        if signature[index] == str:
            parsed_param = parse_string_param(param)
        elif signature[index] == bool:
            parsed_param = bool(int(param))
        elif signature[index] == int:
            parsed_param = int(param)
        elif signature[index] == Decimal:
            try:
                parsed_param = Decimal(param)
            except InvalidOperation as err:
                raise ValueError from err
        elif signature[index] == bytearray:
            parsed_param = parse_byte_param(param)
        else:
            raise ValueError("Invalid parameter type")

        parsed_params.append(parsed_param)

    return parsed_params


def encode_params(*params: ParameterType, force_quotes: bool = False) -> str:
    """Encode a list of parameters for sending to the Host Command service.

    Converts all params to strings, wraps strings in double quotes, and escapes
    double quotes.

    Args:
        params: The parameters to encode.
        force_quotes: Whether to force string params to be wrapped in double quotes.

    Returns:
        The encoded parameters, joined by spaces.

    Raises:
        TypeError: If a parameter is of an unsupported type.
    """
    encoded_params = []
    for value in params:
        if isinstance(value, str):
            encoded_param = encode_string_param(value, force_quotes)
        elif isinstance(value, bool):
            encoded_param = "1" if value else "0"
        elif isinstance(value, (int, float, Decimal)):
            encoded_param = str(value)
        elif isinstance(value, bytearray):
            encoded_param = encode_byte_param(value)
        else:
            raise TypeError(f"Invalid value type: {type(value)}")

        encoded_params.append(encoded_param)

    return " ".join(encoded_params)


def parse_string_param(param: str) -> str:
    """Parse a string parameter from the Host Command service.

    Handles unescaping quotes.

    Args:
        param: The parameter to parse.

    Returns:
        The parsed parameter.
    """
    if param.startswith('"') and param.endswith('"'):
        return param[1:-1].replace('""', '"')

    return param


def encode_string_param(param: str, force_quotes: bool = False) -> str:
    """Encode a string parameter for sending to the Host Command service.

    Wraps the string in double quotes if necessary, and escapes double quotes.

    Args:
        param: The parameter to encode.
        force_quotes: Whether to force the string to be wrapped in double quotes.

    Returns:
        The encoded parameter.
    """
    if '"' in param or " " in param or force_quotes:
        param = param.replace('"', '""')
        return f'"{param}"'

    return param


def parse_byte_param(byte_string: str) -> bytearray:
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


def encode_byte_param(byte_array: bytearray) -> str:
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
