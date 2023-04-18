from dataclasses import dataclass

from ..xml_dataclass import xml_element
from .system_object import SystemObject


@dataclass
class LocationObject(SystemObject):
    area_id: int = xml_element("Area")
    location: str = xml_element("Location")
