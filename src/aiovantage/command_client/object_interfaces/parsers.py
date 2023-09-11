"""Common parsers for object interfaces responses."""

from decimal import Decimal
from enum import IntEnum
from typing import Type, TypeVar

from .base import InterfaceResponse

T = TypeVar("T", bound=IntEnum)


def fixed_to_decimal(value: str) -> Decimal:
    """Convert a Vantage fixed-point value to a Decimal."""
    # Handles both 123000 and 123.000 style fixed-point values
    return Decimal(value.replace(".", "")) / 1000


def parse_fixed(response: InterfaceResponse) -> Decimal:
    """Parse a fixed-point result."""
    return fixed_to_decimal(response.result)


def parse_int(response: InterfaceResponse) -> int:
    """Parse an integer result."""
    return int(response.result)


def parse_bool(response: InterfaceResponse) -> bool:
    """Parse a boolean result."""
    return bool(int(response.result))


def parse_str(response: InterfaceResponse) -> str:
    """Parse a string result."""
    return response.result.rstrip()


def parse_enum(enum_cls: Type[T], response: InterfaceResponse) -> T:
    """Parse an enum result."""
    if response.result.isdigit():
        return enum_cls(int(response.result))

    return enum_cls[response.result]
