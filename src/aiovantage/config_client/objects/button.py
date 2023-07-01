"""Button object."""

from dataclasses import dataclass

from aiovantage.config_client.xml_dataclass import xml_element

from .system_object import SystemObject


@dataclass
class Button(SystemObject):
    """Button object."""

    parent_id: int = xml_element("Parent")
    text1: str = xml_element("Text1")
    text2: str = xml_element("Text2")
    up_task_id: int = xml_element("Up")
    down_task_id: int = xml_element("Down")
    hold_task_id: int = xml_element("Hold")

    @property
    def has_task(self) -> bool:
        """Return True if button has a task assigned."""
        return any(
            task_id != 0
            for task_id in (
                self.up_task_id,
                self.down_task_id,
                self.hold_task_id,
            )
        )

    def __post_init__(self) -> None:
        """Declare state attributes in post init."""
        self.pressed: bool = False
