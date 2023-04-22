from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from aiovantage.aci_client.xml_dataclass import xml_element

from .system_object import SystemObject


@dataclass
class GMem(SystemObject):
    class Type(Enum):
        TEXT = "Text"
        NUMBER = "Number"
        SECONDS = "Seconds"
        DELAY = "Delay"
        LEVEL = "Level"
        BOOL = "bool"
        TEMPERATURE = "DegC"
        LOAD = "Load"
        TASK = "Task"
        DEVICE_UNITS = "DeviceUnits"

    tag: "GMem.Type" = xml_element("Tag")
    persistent: bool = xml_element("Persistent")

    def __post_init__(self) -> None:
        self.value: Optional[Any] = None
