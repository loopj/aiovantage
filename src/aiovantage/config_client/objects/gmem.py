from dataclasses import dataclass
from typing import Union

from aiovantage.config_client.xml_dataclass import xml_element

from .system_object import SystemObject


@dataclass
class GMem(SystemObject):
    tag: str = xml_element("Tag")
    persistent: bool = xml_element("Persistent")

    def __post_init__(self) -> None:
        self.value: Union[int, str, bool, None] = None

    @property
    def is_bool(self) -> bool:
        return self.tag == "bool"

    @property
    def is_str(self) -> bool:
        return self.tag == "Text"

    @property
    def is_int(self) -> bool:
        return self.tag in (
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
        return self.tag in ("Load", "Task")
