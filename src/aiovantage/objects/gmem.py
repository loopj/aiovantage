"""GMem (variable) object."""

from dataclasses import dataclass, field

from .system_object import SystemObject


@dataclass
class GMem(SystemObject):
    """GMem (variable) object."""

    @dataclass
    class Tag:
        type: str
        object: bool = field(
            default=False, metadata={"name": "object", "type": "Attribute"}
        )

    @dataclass
    class Data:
        fixed: bool = field(default=False, metadata={"type": "Attribute"})

    data: Data = field(metadata={"name": "data"})
    persistent: bool
    tag: Tag

    # State
    value: int | str | bool | None = field(default=None, metadata={"type": "Ignore"})

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
