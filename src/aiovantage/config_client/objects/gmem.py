"""GMem (variable) object."""

from dataclasses import dataclass
from typing import Union

from aiovantage.config_client.xml_dataclass import xml_attribute, xml_element, xml_text

from .system_object import SystemObject


@dataclass
class GMem(SystemObject):
    """GMem (variable) object."""

    @dataclass
    class Tag:
        """GMem tag."""

        type: str = xml_text()
        object: bool = xml_attribute("object", default=False)

    @dataclass
    class Data:
        """GMem data."""

        fixed: bool = xml_attribute("Fixed", default=False)

    data: Data = xml_element("data")
    persistent: bool = xml_element("Persistent")
    tag: Tag = xml_element("Tag")

    def __post_init__(self) -> None:
        """Declare state attributes in post init."""
        self.value: Union[int, str, bool, None] = None

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
