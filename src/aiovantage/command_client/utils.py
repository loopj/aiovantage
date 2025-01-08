"""Utility functions for the Host Command service client."""

import datetime as dt
import re
import struct
from decimal import Decimal
from enum import IntEnum
from types import NoneType
from typing import Any, TypeVar, cast, get_type_hints

TOKEN_PATTERN = re.compile(r'"([^""]*(?:""[^""]*)*)"|(\{.*?\})|(\[.*?\])|(\S+)')

ParameterType = str | bool | int | float | bytearray | Decimal | IntEnum | dt.datetime

T = TypeVar("T")


def tokenize_response(string: str) -> list[str]:
    """Tokenize a response from the Host Command service.

    Handles quoted strings and byte arrays as single tokens.

    Args:
        string: The response string to tokenize.

    Returns:
        A list of string tokens.
    """
    tokens: list[str] = []
    for match in TOKEN_PATTERN.finditer(string):
        token = match.group(0)

        # Remove quotes from quoted strings, and unescape quotes
        if token.startswith('"') and token.endswith('"'):
            token = token[1:-1].replace('""', '"')

        tokens.append(token)

    return tokens


def parse_param(arg: str, klass: type[T]) -> T:
    """Parse a single response parameter from the Host Command service.

    Args:
        arg: The parameter to parse.
        klass: The expected parameter type.

    Returns:
        The parsed parameter.

    Raises:
        ValueError: If the parameter is of an unsupported type.
    """
    if klass is int:
        parsed = int(arg)
    elif klass is bool:
        parsed = bool(int(arg))
    elif klass is str:
        parsed = parse_string_param(arg)
    elif klass is bytearray:
        parsed = parse_byte_param(arg)
    elif klass is dt.datetime:
        parsed = dt.datetime.fromtimestamp(int(arg))
    elif klass is Decimal:
        parsed = parse_fixed_param(arg)
    elif klass is float:
        parsed = float(arg)
    elif issubclass(klass, IntEnum):
        # Support both integer and string values for IntEnum
        parsed = klass(int(arg)) if arg.isdigit() else klass[arg]
    else:
        raise ValueError(f"Unsupported type: {klass}")

    return cast(T, parsed)


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

    def encode(param: ParameterType) -> str:
        match param:
            case str():
                return encode_string_param(param, force_quotes=force_quotes)
            case bool():
                return "1" if param else "0"
            case IntEnum():
                return str(param.value)
            case int():
                return str(param)
            case float():
                return f"{param:.3f}"
            case Decimal():
                return f"{param:.3f}"
            case bytearray():
                return encode_byte_param(param)
            case dt.datetime():
                return str(int(param.timestamp()))

    return " ".join(encode(param) for param in params)


def parse_fixed_param(param: str) -> Decimal:
    """Parse a fixed-point parameter from the Host Command service."""
    # Handles both 123000 and 123.000 style fixed-point values
    return Decimal(param.replace(".", "")) / 1000


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


def encode_string_param(param: str, *, force_quotes: bool = False) -> str:
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

    "Bytes" parameters are sent as a string of signed 32-bit integers, separated by
    commas or spaces, and wrapped in curly or square brackets.

    Args:
        byte_string: The byte array parameter, as a string.

    Returns:
        The byte array.
    """
    # Extract all integer tokens from the string
    tokens = [int(x) for x in re.findall(r"-?\d+", byte_string)]

    # Convert each token to a signed 32-bit integer and create a byte array
    byte_array = bytearray()
    for token in tokens:
        signed_int = struct.pack("i", token)
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
    tokens = [
        str(struct.unpack("i", byte_array[i : i + 4])[0])
        for i in range(0, len(byte_array), 4)
    ]

    # Join the tokens with commas and wrap in curly braces
    return "{" + ",".join(tokens) + "}"


def parse_object_response(
    result: str, *args: str, as_type: type[T] | None = None
) -> T | None:
    """Parse an object interface "INVOKE" response or status message.

    Args:
        result: The result of the command.
        args: The arguments that were sent with the command.
        as_type: The expected return type of the method.

    Returns:
        A response parsed into the expected type.
    """
    # -> R:INVOKE <id> <result> <Interface.Method> <arg1> <arg2> ...
    # -> EL: <id> <Interface.Method> <result> <arg1> <arg2> ...
    # -> S:STATUS <id> <Interface.Method> <result> <arg1> <arg2> ...

    # If no type is specified, return early
    if as_type in (None, NoneType):
        return None

    # Otherwise, parse the result into the expected type
    if type_hints := get_type_hints(as_type):
        # Some methods return multiple values, in the result and in the arguments
        # To support this, if the signature is an object with type hints, we'll assume
        # we are packing the values into the attributes of the object
        # The "result" is packed into the first argument, followed by the rest of the arguments
        parsed_values: list[Any] = []
        for arg, klass in zip([result, *args], type_hints.values(), strict=True):
            parsed_values.append(parse_param(arg, klass))

        parsed_response = as_type(*parsed_values)
    else:
        # Otherwise, parse a single return value
        parsed_response = parse_param(result, as_type)

    # Return the parsed result
    return parsed_response
