from dataclasses import dataclass
from typing import Optional

from ..xml_dataclass import xml_element
from .system_object import SystemObject


@dataclass
class LocationObject(SystemObject):
    area: Optional[int] = xml_element("Area", default=None)
    location: Optional[str] = xml_element("Location", default=None)
