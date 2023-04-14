from dataclasses import dataclass
from typing import Optional

from ..xml_dataclass import xml_element
from .system_object import SystemObject


@dataclass
class StationBus(SystemObject):
    parent: Optional[int] = xml_element("Parent", default=None)
