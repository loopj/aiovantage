from dataclasses import dataclass
from typing import Optional, Tuple

from ..xml_dataclass import xml_element
from .location_object import LocationObject


@dataclass
class RGBLoad(LocationObject):
    color_type: str = xml_element("ColorType")
    min_temp: int = xml_element("MinTemp")
    max_temp: int = xml_element("MaxTemp")

    def __post_init__(self) -> None:
        self.level: Optional[float] = None
        self.hs: Optional[Tuple[int, int]] = None
        self.rgb: Optional[Tuple[int, int, int]] = None
        self.rgbw: Optional[Tuple[int, int, int, int]] = None
        self.color_temp: Optional[int] = None


@dataclass
class DGColorLoad(RGBLoad):
    class Meta:
        name = "Vantage.DGColorLoad"


@dataclass
class DDGColorLoad(RGBLoad):
    class Meta:
        name = "Vantage.DDGColorLoad"
