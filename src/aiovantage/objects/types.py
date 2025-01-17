"""Parent type."""

from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Parent:
    """Parent type."""

    id: int
    position: int = field(metadata={"type": "Attribute"})


@dataclass(kw_only=True)
class Array:
    """Array type."""

    @dataclass(kw_only=True)
    class StringData:
        string: str = ""
        size: int = field(metadata={"name": "size", "type": "Attribute"})

    @dataclass(kw_only=True)
    class BytesData:
        bytes: str = ""
        size: int = field(metadata={"name": "size", "type": "Attribute"})

    val: int | None = field(default=None, metadata={"name": "val"})
    string: StringData | None = field(default=None, metadata={"name": "string"})
    bytes: BytesData | None = field(default=None, metadata={"name": "bytes"})
    array: "Array | None" = field(default=None, metadata={"name": "array"})
