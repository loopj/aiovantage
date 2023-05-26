from dataclasses import dataclass
from enum import Enum
from typing import Optional

from aiovantage.config_client.xml_dataclass import xml_element

from .system_object import SystemObject


@dataclass
class Button(SystemObject):
    class State(Enum):
        UP = 0
        DOWN = 1

    parent_id: int = xml_element("Parent")
    text1: str = xml_element("Text1")
    text2: str = xml_element("Text2")
    up_task_id: int = xml_element("Up")
    down_task_id: int = xml_element("Down")
    hold_task_id: int = xml_element("Hold")

    @property
    def has_task(self) -> bool:
        return any(
            task_id != 0
            for task_id in (
                self.up_task_id,
                self.down_task_id,
                self.hold_task_id,
            )
        )

    def __post_init__(self) -> None:
        self.state: Optional["Button.State"] = None
