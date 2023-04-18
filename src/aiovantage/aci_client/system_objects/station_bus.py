from dataclasses import dataclass

from ..xml_dataclass import xml_element
from .system_object import SystemObject


@dataclass
class StationBus(SystemObject):
    parent_id: int = xml_element("Parent")
