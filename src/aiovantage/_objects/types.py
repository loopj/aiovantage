"""Common types."""

from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(kw_only=True)
class Parent:
    """Vantage parent type."""

    vid: int
    position: int = field(metadata={"type": "Attribute"})


@dataclass(kw_only=True)
class Array:
    """Vantage array type."""

    @dataclass(kw_only=True)
    class StringData:
        string: str = ""
        size: int = field(metadata={"name": "size", "type": "Attribute"})

    @dataclass(kw_only=True)
    class BytesData:
        bytes: str = ""
        size: int = field(metadata={"name": "size", "type": "Attribute"})

    val: int | Decimal | None = field(default=None, metadata={"name": "val"})
    string: StringData | None = field(default=None, metadata={"name": "string"})
    bytes: BytesData | None = field(default=None, metadata={"name": "bytes"})
    array: "Array | None" = field(default=None, metadata={"name": "array"})
