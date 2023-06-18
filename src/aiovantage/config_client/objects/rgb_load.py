"""RGB load object."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from aiovantage.config_client.xml_dataclass import xml_element

from .location_object import LocationObject

# This isn't strictly a Vantage object type, but this helps us avoid
# code duplication in RGBLoad-like objects.


@dataclass
class RGBLoad(LocationObject):
    """RGB load object."""

    class ColorType(Enum):
        """Color type."""

        RGB = "RGB"
        RGBW = "RGBW"
        HSL = "HSL"
        HSIC = "HSIC"
        CCT = "CCT"
        COLOR_CHANNEL = "Color Channel"

    color_type: ColorType = xml_element("ColorType")
    min_temp: int = xml_element("MinTemp")
    max_temp: int = xml_element("MaxTemp")

    def __post_init__(self) -> None:
        """Post init."""

        self.hsl: Optional[Tuple[int, int, int]] = None
        self.rgb: Optional[Tuple[int, int, int]] = None
        self.rgbw: Optional[Tuple[int, int, int, int]] = None
        self.level: Optional[int] = None
        self.color_temp: Optional[int] = None

    @property
    def is_on(self) -> bool:
        """Return True if the load is on."""
        return bool(self.level)

    @property
    def is_rgb(self) -> bool:
        """Return True if the load is an RGB(W) load."""
        return self.color_type in (
            RGBLoad.ColorType.RGB,
            RGBLoad.ColorType.RGBW,
            RGBLoad.ColorType.HSL,
        )

    @property
    def is_cct(self) -> bool:
        """Return True if the load is a CCT load."""
        return self.color_type == RGBLoad.ColorType.CCT
