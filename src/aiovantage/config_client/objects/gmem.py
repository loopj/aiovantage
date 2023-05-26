from dataclasses import dataclass
from enum import Enum
from typing import Union

from aiovantage.config_client.xml_dataclass import xml_element

from .system_object import SystemObject


@dataclass
class GMem(SystemObject):
    class Type(Enum):
        BOOL = "bool"
        DELAY = "Delay"
        DEVICE_UNITS = "DeviceUnits"
        LEVEL = "Level"
        LOAD = "Load"
        NUMBER = "Number"
        SECONDS = "Seconds"
        TASK = "Task"
        TEMPERATURE = "DegC"
        TEXT = "Text"

    tag: "GMem.Type" = xml_element("Tag")
    persistent: bool = xml_element("Persistent")

    def __post_init__(self) -> None:
        self.value: Union[int, bool, str, None] = None

    @property
    def is_bool(self) -> bool:
        return self.tag == self.Type.BOOL

    @property
    def is_str(self) -> bool:
        return self.tag == self.Type.TEXT

    @property
    def is_int(self) -> bool:
        return self.tag in (
            self.Type.DELAY,
            self.Type.DEVICE_UNITS,
            self.Type.LEVEL,
            self.Type.LOAD,
            self.Type.NUMBER,
            self.Type.SECONDS,
            self.Type.TASK,
            self.Type.TEMPERATURE,
        )

    @property
    def is_object_id(self) -> bool:
        return self.tag in (self.Type.LOAD, self.Type.TASK)
