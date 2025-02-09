import datetime as dt
import re
import struct
from abc import ABC, abstractmethod
from decimal import Decimal
from enum import IntEnum
from typing import Any

from typing_extensions import override


class BaseConverter(ABC):
    """Abstract base class for Host Command service data converters."""

    @staticmethod
    @abstractmethod
    def serialize(value: Any, **kwargs: Any) -> str:
        """Serialize a value to a string representation."""

    @staticmethod
    @abstractmethod
    def deserialize(value: str, **kwargs: Any) -> Any:
        """Deserialize a string representation to a value."""


class StringConverter(BaseConverter):
    """String parameter converter.

    Vantage "string" parameters are either single words or quoted strings.

    Quoted strings are wrapped in double quotes, and any double quotes within
    the string are escaped with an additional double quote.
    """

    @override
    @staticmethod
    def deserialize(value: str, **_kwargs: Any) -> str:
        if value.startswith('"') and value.endswith('"'):
            # Unwrap and unescape the string, if it's wrapped in double quotes
            return value[1:-1].replace('""', '"')

        return value

    @override
    @staticmethod
    def serialize(value: str, **kwargs: Any) -> str:
        # Escape any double quotes in the string
        value = value.replace('"', '""')

        # Wrap the string in double quotes
        return f'"{value}"'


class BoolConverter(BaseConverter):
    """Bool parameter converter.

    Vantage "bool" parameters are encoded as either "0" or "1".
    """

    @override
    @staticmethod
    def deserialize(value: str, **_kwargs: Any) -> bool:
        return bool(int(value))

    @override
    @staticmethod
    def serialize(value: bool, **_kwargs: Any) -> str:
        return "1" if value else "0"


class IntConverter(BaseConverter):
    """An int converter."""

    @override
    @staticmethod
    def deserialize(value: str, **kwargs: Any) -> int:
        """Deserialize an int value."""
        return int(value)

    @override
    @staticmethod
    def serialize(value: int, **kwargs: Any) -> str:
        """Serialize an int value."""
        return str(value)


class FloatConverter(BaseConverter):
    """A float converter.

    If these types are tagged as "fixed", they should be handled as Decimal values.
    """

    @override
    @staticmethod
    def deserialize(value: str, **kwargs: Any) -> float:
        return float(value)

    @override
    @staticmethod
    def serialize(value: float, **kwargs: Any) -> str:
        precision = kwargs.get("precision", 3)
        return f"{value:.{precision}f}"


class DecimalConverter(BaseConverter):
    """A Decimal converter.

    Vantage "fixed" parameters are encoded as a string representation of a
    fixed-point value, with three decimal places.
    """

    @override
    @staticmethod
    def deserialize(value: str, **kwargs: Any) -> Decimal:
        # Handle both forms of fixed-point values:
        # - "123.456" (INVOKE replies)
        # - "123456"  (S:STATUS messages)
        return Decimal(value.replace(".", "")) / 1000

    @override
    @staticmethod
    def serialize(value: Decimal, **kwargs: Any) -> str:
        precision = kwargs.get("precision", 3)
        return f"{value:.{precision}f}"


class BytesConverter(BaseConverter):
    """A bytes converter.

    Vantage "bytes" parameters are encoded as a string of signed 32-bit integers,
    separated by commas or spaces, and wrapped in curly or square braces.
    """

    @override
    @staticmethod
    def deserialize(value: str, **_kwargs: Any) -> bytes:
        # Extract all integer tokens from the string
        tokens = [int(x) for x in re.findall(r"-?\d+", value)]

        # Convert each token to a signed 32-bit integer and concatenate them into bytes
        return b"".join(struct.pack("i", token) for token in tokens)

    @override
    @staticmethod
    def serialize(value: bytes, **_kwargs: Any) -> str:
        # Pad the data to a multiple of 4 bytes
        value += b"\x00" * (-len(value) % 4)

        # Convert each signed 32-bit integer in the byte array to a string token
        tokens = [
            str(struct.unpack("i", value[i : i + 4])[0])
            for i in range(0, len(value), 4)
        ]

        # Join the tokens with commas and wrap in curly braces
        return "{" + ",".join(tokens) + "}"


class DateTimeConverter(BaseConverter):
    """A datetime converter.

    Vantage "Time" parameters are encoded as a Unix timestamp.
    """

    @override
    @staticmethod
    def deserialize(value: str, **_kwargs: Any) -> dt.datetime:
        return dt.datetime.fromtimestamp(int(value), dt.timezone.utc)

    @override
    @staticmethod
    def serialize(value: dt.datetime, **_kwargs: Any) -> str:
        return str(int(value.timestamp()))


class IntEnumConverter(BaseConverter):
    """An IntEnum converter.

    Vantage "Enum" values are encoded as either their integer or string
    representation.

    String representations are either lowercase single words or PascalCase.
    """

    @override
    @staticmethod
    def deserialize(value: str, **kwargs: Any) -> Any:
        enum_type = kwargs.get("data_type")
        if enum_type is None or not issubclass(enum_type, IntEnum):
            raise ValueError("IntEnumConverter requires a data_type argument")

        # Handle integer representations of enum values
        if value.isdigit():
            return enum_type(int(value))

        # Handle string representations of enum values.
        return enum_type[value]

    @override
    @staticmethod
    def serialize(value: Any, **kwargs: Any) -> str:
        # The API accepts either the integer or string representation of the enum
        # We'll always serialize to the integer representation for simplicity
        return str(value.value)


# Map of data types to their respective converters
CONVERTER_MAP: dict[type, type[BaseConverter]] = {
    str: StringConverter,
    int: IntConverter,
    bool: BoolConverter,
    float: FloatConverter,
    Decimal: DecimalConverter,
    bytes: BytesConverter,
    dt.datetime: DateTimeConverter,
    IntEnum: IntEnumConverter,
}


def _get_converter(data_type: type) -> type[BaseConverter]:
    # Check if the data type is directly registered
    if data_type in CONVERTER_MAP:
        return CONVERTER_MAP[data_type]

    # If not, check the MRO for a registered type
    for mro in data_type.__mro__[1:-1]:
        if mro in CONVERTER_MAP:
            return CONVERTER_MAP[mro]

    raise ValueError(f"No converter found for {data_type}")


# Token splitting regular expression
TOKEN_PATTERN = re.compile(r'"([^""]*(?:""[^""]*)*)"|(\{.*?\})|(\[.*?\])|(\S+)')


class Converter:
    """Host Command service data conversion functions."""

    @staticmethod
    def deserialize(data_type: type, value: str, **kwargs: Any) -> Any:
        """Deserialize a token from the Host Command service.

        Args:
            data_type: The data type to deserialize the value to.
            value: The string data to deserialize.
            **kwargs: Additional deserialization arguments.

        Returns:
            The deserialized object.
        """
        converter = _get_converter(data_type)
        return converter.deserialize(value, data_type=data_type, **kwargs)

    @staticmethod
    def serialize(value: Any, **kwargs: Any) -> str:
        """Serialize an object to a string token for the Host Command service.

        Args:
            value: The value to serialize to a string.
            **kwargs: Additional serialization arguments.

        Returns:
            A string representation of the object.
        """
        converter = _get_converter(value.__class__)
        return converter.serialize(value, **kwargs)

    @staticmethod
    def tokenize(string: str) -> list[str]:
        """Tokenize a response from the Host Command service.

        Handles quoted strings and byte arrays as single tokens.

        Args:
            string: The response string to tokenize.

        Returns:
            A list of string tokens.
        """
        return [match.group(0) for match in TOKEN_PATTERN.finditer(string)]
