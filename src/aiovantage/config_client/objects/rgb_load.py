from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple, Optional

from aiovantage.config_client.xml_dataclass import xml_element

from .location_object import LocationObject


@dataclass
class RGBLoad(LocationObject):
    class ColorType(Enum):
        RGB = "RGB"
        RGBW = "RGBW"
        HSL = "HSL"
        HSIC = "HSIC"
        CCT = "CCT"
        COLOR_CHANNEL = "Color Channel"

    class RGBValue(NamedTuple):
        red: int
        green: int
        blue: int

    class RGBWValue(NamedTuple):
        red: int
        green: int
        blue: int
        white: int

    class HSLValue(NamedTuple):
        hue: int
        saturation: int
        lightness: int

    color_type: ColorType = xml_element("ColorType")
    min_temp: int = xml_element("MinTemp")
    max_temp: int = xml_element("MaxTemp")

    def __post_init__(self) -> None:
        self.hsl: Optional[RGBLoad.HSLValue] = None
        self.rgb: Optional[RGBLoad.RGBValue] = None
        self.rgbw: Optional[RGBLoad.RGBWValue] = None
        self.cct_temp: Optional[int] = None
        self.cct_level: Optional[int] = None

    @property
    def is_on(self) -> bool:
        """
        Return whether the load is on.
        """

        return bool(self.level)

    @property
    def level(self) -> Optional[float]:
        """
        Return the level of the load, as a percentage (0-100).
        """

        if self.color_type == RGBLoad.ColorType.HSL:
            if self.hsl is None:
                return None

            return self.hsl.lightness

        elif self.color_type == RGBLoad.ColorType.RGB:
            if self.rgb is None:
                return None

            return round(max(self.rgb) / 255 * 100)

        elif self.color_type == RGBLoad.ColorType.RGBW:
            if self.rgbw is None:
                return None

            return round(max(self.rgbw) / 255 * 100)

        elif self.color_type == RGBLoad.ColorType.CCT:
            if self.cct_level is None:
                return None

            return self.cct_level

        return None
