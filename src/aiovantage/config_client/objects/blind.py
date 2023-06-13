from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from aiovantage.config_client.xml_dataclass import xml_attribute, xml_element

from .location_object import LocationObject

@dataclass
class Blind(LocationObject):
    parent_id: Optional[int] = xml_element("Parent", default=None)
    orientation: Optional[str] = xml_attribute("ShadeOrientation", default=None)
    type: Optional[str] = xml_attribute("ShadeType", default=None)

    def __post_init__(self) -> None:
        self.position: Optional[Decimal] = None
