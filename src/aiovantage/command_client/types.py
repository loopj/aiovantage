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

    def deserialize(self, value: Any, **_kwargs: Any) -> str:
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

    def deserialize(self, value: Any, **_kwargs: Any) -> bool:
        """Deserialize a bool value."""
        return bool(int(value))

    def serialize(self, value: bool, **_kwargs: Any) -> str:
        """Serialize a bool value."""
        return "1" if value else "0"


class IntConverter(Converter):
    """An int converter."""

    def deserialize(self, value: Any, **kwargs: Any) -> int:
        """Deserialize an int value."""
        return int(value)

    def serialize(self, value: int, **kwargs: Any) -> str:
        """Serialize an int value."""
        return str(value)


class FloatConverter(Converter):
    """A float converter.

    Common Vantage "float" types include those labeled as:
        Seconds, Level, Celsius, MPH, Footcandles, and DeviceUnits

    If these types are tagged as "fixed", they should be handled as Decimal values.
    """

    def deserialize(self, value: Any, **kwargs: Any) -> float:
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

    For example, the Decimal value 123.456 would be encoded as:
        "123.456" (In a reply to an INVOKE command)
        "123456"  (In an S:STATUS message)
    """

    def deserialize(self, value: Any, **kwargs: Any) -> Decimal:
        """Deserialize a Decimal value."""
        return Decimal(value.replace(".", "")) / 1000

    def serialize(self, value: Decimal, **kwargs: Any) -> str:
        """Serialize a Decimal value."""
        precision = kwargs.get("precision", 3)
        return f"{value:.{precision}f}"


class ByteArrayConverter(Converter):
    """A bytearray converter.

    Vantage "bytes" parameters are encoded as a string of signed 32-bit integers,
    separated by commas or spaces, and wrapped in curly or square braces.

    Byte arrays representing strings have a header of {1, 34}
    """

    def deserialize(self, value: Any, **_kwargs: Any) -> bytearray:
        """Deserialize a byte array parameter."""
        # Extract all integer tokens from the string
        tokens = [int(x) for x in re.findall(r"-?\d+", value)]

        # Convert each token to a signed 32-bit integer and create a byte array
        byte_array = bytearray()
        for token in tokens:
            signed_int = struct.pack("i", token)
            byte_array.extend(signed_int)

        return byte_array

    def serialize(self, value: bytearray, **_kwargs: Any) -> str:
        """Serialize a byte array parameter."""
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

    def deserialize(self, value: Any, **_kwargs: Any) -> dt.datetime:
        """Deserialize a datetime value."""
        return dt.datetime.fromtimestamp(int(value), dt.timezone.utc)

    def serialize(self, value: dt.datetime, **_kwargs: Any) -> str:
        """Serialize a datetime value."""
        return str(int(value.timestamp()))


class IntEnumConverter(Converter):
    """An IntEnum converter.

    "IntEnum" type parameters may be encoded as either their integer or string
    representations.
    """

    def deserialize(self, value: Any, **kwargs: Any) -> Any:
        """Deserialize an IntEnum value."""
        enum_type = kwargs.get("data_type")
        if enum_type is None or not issubclass(enum_type, IntEnum):
            raise ValueError("IntEnumConverter requires a data_type argument")

        return enum_type(int(value)) if value.isdigit() else enum_type[value]

    def serialize(self, value: Any, **kwargs: Any) -> str:
        """Serialize an IntEnum value."""
        return str(value.value)


# Create a global converter registry, and register the default converters
converter = ConverterRegistry()
converter.register(str, StringConverter())
converter.register(int, IntConverter())
converter.register(bool, BoolConverter())
converter.register(float, FloatConverter())
converter.register(Decimal, DecimalConverter())
converter.register(bytearray, ByteArrayConverter())
converter.register(dt.datetime, DateTimeConverter())
converter.register(IntEnum, IntEnumConverter())