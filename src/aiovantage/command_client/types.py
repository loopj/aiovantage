"""Command client data conversion utilities."""

import datetime as dt
import re
import struct
from abc import ABC, abstractmethod
from decimal import Decimal
from enum import IntEnum
from typing import Any

TOKEN_PATTERN = re.compile(r'"([^""]*(?:""[^""]*)*)"|(\{.*?\})|(\[.*?\])|(\S+)')


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


class Converter(ABC):
    """Abstract data converter class."""

    @abstractmethod
    def serialize(self, value: Any, **kwargs: Any) -> str: ...  # noqa: D102

    @abstractmethod
    def deserialize(self, value: str, **kwargs: Any) -> Any: ...  # noqa: D102


class ConverterRegistry:
    """A registry for data converters."""

    registry: dict[type, Converter]

    def __init__(self):
        """Initialize the registry."""
        self.registry = {}

    def register(self, data_type: type, converter: Converter) -> None:
        """Register a converter for a data type.

        Args:
            data_type: The type of data to convert.
            converter: The converter instance.
        """
        self.registry[data_type] = converter

    def get_converter(self, data_type: type) -> Converter:
        """Get the converter for a data type.

        Args:
            data_type: The type of data to convert.

        Returns:
            The converter for the data type.
        """
        # Check if the data type is directly registered
        if data_type in self.registry:
            return self.registry[data_type]

        # If not, check the MRO for a registered type
        for mro in data_type.__mro__[1:-1]:
            if mro in self.registry:
                return self.registry[mro]

        raise ValueError(f"No converter found for {data_type}")

    def deserialize(self, data_type: type, value: str, **kwargs: Any) -> Any:
        """Deserialize a string representation to an object.

        Args:
            data_type: The type of data to convert.
            value: The string data to deserialize.
            **kwargs: Additional deserialization arguments.

        Returns:
            The deserialized object.
        """
        converter = self.get_converter(data_type)
        return converter.deserialize(value, data_type=data_type, **kwargs)

    def serialize(self, value: Any, **kwargs: Any) -> str:
        """Serialize an object to a string representation.

        Args:
            value: The value to serialize to a string.
            **kwargs: Additional serialization arguments.

        Returns:
            A string representation of the object.
        """
        converter = self.get_converter(value.__class__)
        return converter.serialize(value, **kwargs)


class StringConverter(Converter):
    """String parameter converter.

    Vantage "string" parameters are either single words or quoted strings.

    Quoted strings are wrapped in double quotes, and any double quotes within
    the string are escaped with an additional double quote.
    """

    def deserialize(self, value: str, **_kwargs: Any) -> str:
        """Deserialize a string value."""
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1].replace('""', '"')

        return value

    def serialize(self, value: str, **kwargs: Any) -> str:
        """Serialize a string value."""
        force_quotes = kwargs.get("force_quotes", False)

        if '"' in value or " " in value or force_quotes:
            value = value.replace('"', '""')
            return f'"{value}"'

        return value


class BoolConverter(Converter):
    """Bool parameter converter.

    Vantage "bool" parameters are encoded as either "0" or "1".
    """

    def deserialize(self, value: str, **_kwargs: Any) -> bool:
        """Deserialize a bool value."""
        return bool(int(value))

    def serialize(self, value: bool, **_kwargs: Any) -> str:
        """Serialize a bool value."""
        return "1" if value else "0"


class IntConverter(Converter):
    """An int converter."""

    def deserialize(self, value: str, **kwargs: Any) -> int:
        """Deserialize an int value."""
        return int(value)

    def serialize(self, value: int, **kwargs: Any) -> str:
        """Serialize an int value."""
        return str(value)


class FloatConverter(Converter):
    """A float converter.

    If these types are tagged as "fixed", they should be handled as Decimal values.
    """

    def deserialize(self, value: str, **kwargs: Any) -> float:
        """Deserialize a float value."""
        return float(value)

    def serialize(self, value: float, **kwargs: Any) -> str:
        """Serialize a float value."""
        precision = kwargs.get("precision", 3)
        return f"{value:.{precision}f}"


class DecimalConverter(Converter):
    """A Decimal converter.

    Vantage "fixed" parameters are encoded as a string representation of a
    fixed-point value, with three decimal places.
    """

    def deserialize(self, value: str, **kwargs: Any) -> Decimal:
        """Deserialize a Decimal value."""
        # Handle both forms of fixed-point values:
        # - "123.456" (INVOKE replies)
        # - "123456"  (S:STATUS messages)
        return Decimal(value.replace(".", "")) / 1000

    def serialize(self, value: Decimal, **kwargs: Any) -> str:
        """Serialize a Decimal value."""
        precision = kwargs.get("precision", 3)
        return f"{value:.{precision}f}"


class BytesConverter(Converter):
    """A bytes converter.

    Vantage "bytes" parameters are encoded as a string of signed 32-bit integers,
    separated by commas or spaces, and wrapped in curly or square braces.
    """

    def deserialize(self, value: str, **_kwargs: Any) -> bytes:
        """Deserialize a bytes parameter."""
        # Extract all integer tokens from the string
        tokens = [int(x) for x in re.findall(r"-?\d+", value)]

        # Convert each token to a signed 32-bit integer and concatenate them into bytes
        return b"".join(struct.pack("i", token) for token in tokens)

    def serialize(self, value: bytes, **_kwargs: Any) -> str:
        """Serialize a bytes parameter."""
        # Pad the data to a multiple of 4 bytes
        value += b"\x00" * (-len(value) % 4)

        # Convert each signed 32-bit integer in the byte array to a string token
        tokens = [
            str(struct.unpack("i", value[i : i + 4])[0])
            for i in range(0, len(value), 4)
        ]

        # Join the tokens with commas and wrap in curly braces
        return "{" + ",".join(tokens) + "}"


class DateTimeConverter(Converter):
    """A datetime converter.

    Vantage "Time" parameters are encoded as a Unix timestamp.
    """

    def deserialize(self, value: str, **_kwargs: Any) -> dt.datetime:
        """Deserialize a datetime value."""
        return dt.datetime.fromtimestamp(int(value), dt.timezone.utc)

    def serialize(self, value: dt.datetime, **_kwargs: Any) -> str:
        """Serialize a datetime value."""
        return str(int(value.timestamp()))


class IntEnumConverter(Converter):
    """An IntEnum converter.

    Vantage "Enum" values are encoded as either their integer or string
    representation.

    String representations are either lowercase single words or PascalCase.
    """

    def deserialize(self, value: str, **kwargs: Any) -> Any:
        """Deserialize an IntEnum value."""
        enum_type = kwargs.get("data_type")
        if enum_type is None or not issubclass(enum_type, IntEnum):
            raise ValueError("IntEnumConverter requires a data_type argument")

        # Handle integer representations of enum values
        if value.isdigit():
            return enum_type(int(value))

        # Handle string representations of enum values.
        return enum_type[value]

    def serialize(self, value: Any, **kwargs: Any) -> str:
        """Serialize an IntEnum value."""
        # The API accepts either the integer or string representation of the enum
        # We'll always serialize to the integer representation for simplicity
        return str(value.value)


# Create a global converter registry, and register the default converters
converter = ConverterRegistry()
converter.register(str, StringConverter())
converter.register(int, IntConverter())
converter.register(bool, BoolConverter())
converter.register(float, FloatConverter())
converter.register(bytes, BytesConverter())
converter.register(Decimal, DecimalConverter())
converter.register(dt.datetime, DateTimeConverter())
converter.register(IntEnum, IntEnumConverter())
