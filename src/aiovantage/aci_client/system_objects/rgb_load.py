from dataclasses import dataclass

from ..xml_dataclass import xml_element
from .location_object import LocationObject


@dataclass
class RGBLoad(LocationObject):
    color_type: str = xml_element("ColorType")


@dataclass
class DGColorLoad(RGBLoad):
    class Meta:
        name = "Vantage.DGColorLoad"


@dataclass
class DDGColorLoad(RGBLoad):
    class Meta:
        name = "Vantage.DDGColorLoad"
