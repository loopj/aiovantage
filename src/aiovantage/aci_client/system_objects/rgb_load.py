from dataclasses import dataclass
from typing import Optional, Tuple

from ..xml_dataclass import xml_element
from .location_object import LocationObject


@dataclass
class RGBLoad(LocationObject):
    color_type: str = xml_element("ColorType")

    def __post_init__(self) -> None:
        self.rgb: Optional[Tuple[int, int, int]] = None


@dataclass
class DGColorLoad(RGBLoad):
    class Meta:
        name = "Vantage.DGColorLoad"


@dataclass
class DDGColorLoad(RGBLoad):
    class Meta:
        name = "Vantage.DDGColorLoad"
