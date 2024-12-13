"""GMem (variable) object."""

from dataclasses import dataclass, field

from . import SystemObject


@dataclass
class Data:
    """The data contained in the GMem object."""

    @dataclass
    class StringData:
        value: str
        size: int | None = field(
            default=None,
            metadata={"name": "size", "type": "Attribute"},
        )

    @dataclass
    class ByteData:
        value: bytes = field(metadata={"format": "base16"})
        size: int | None = field(
            default=None,
            metadata={"name": "size", "type": "Attribute"},
        )

    val: int | None = field(default=None, metadata={"name": "val"})
    string: StringData | None = field(default=None, metadata={"name": "string"})
    bytes: ByteData | None = field(default=None, metadata={"name": "bytes"})
    fixed: bool = field(default=False, metadata={"type": "Attribute"})


@dataclass
class Tag:
    """The type of the GMem object."""

    type: str
    object: bool = field(
        default=False,
        metadata={"name": "object", "type": "Attribute"},
    )


@dataclass
class GMem(SystemObject):
    """GMem (variable) object."""

    data: Data = field(metadata={"name": "data"})
    persistent: bool
    tag: Tag

    # Convenience property to store the latest value of the GMem
    # Not a part of the true object schema
    value: int | str | bool | None = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    @property
    def is_bool(self) -> bool:
        """Return True if GMem is boolean type."""
        return self.tag.type == "bool"

    @property
    def is_str(self) -> bool:
        """Return True if GMem is string type."""
        return self.tag.type == "Text"

    @property
    def is_int(self) -> bool:
        """Return True if GMem is integer type."""
        return self.tag.type in (
            "Delay",
            "DeviceUnits",
            "Level",
            "Load",
            "Number",
            "Seconds",
            "Task",
            "DegC",
        )

    @property
    def is_object_id(self) -> bool:
        """Return True if GMem is a pointer to an object."""
        return self.tag.object

    @property
    def is_fixed(self) -> bool:
        """Return True if GMem is a fixed point number."""
        return self.data.fixed
