"""Button object."""

from dataclasses import dataclass

from aiovantage.config_client.xml_dataclass import xml_element

from .child_object import ChildObject
from .system_object import SystemObject


@dataclass
class Button(SystemObject, ChildObject):
    """Button object."""

    text1: str = xml_element("Text1")
    text2: str = xml_element("Text2")
    up_id: int = xml_element("Up")
    down_id: int = xml_element("Down")
    hold_id: int = xml_element("Hold")

    @property
    def has_listener(self) -> bool:
        """Return True if button has a task assigned."""
        return any(task_id for task_id in (self.up_id, self.down_id, self.hold_id))

    def __post_init__(self) -> None:
        """Declare state attributes in post init."""
        self.pressed: bool = False
