"""GMem (variable) object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces import GMemInterface

from .system_object import SystemObject
from .types import Array


@dataclass(kw_only=True)
class GMem(SystemObject, GMemInterface):
    """GMem (variable) object."""

    @dataclass
    class Data(Array):
        fixed: bool = field(default=False, metadata={"type": "Attribute"})

    @dataclass
    class Tag:
        type: str
        object: bool = field(
            default=False, metadata={"name": "object", "type": "Attribute"}
        )

    category: int
    data: Data = field(metadata={"name": "data"})
    persistent: bool = True
    tag: Tag

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
