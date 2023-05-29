from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

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

    color_type: ColorType = xml_element("ColorType")
    min_temp: int = xml_element("MinTemp")
    max_temp: int = xml_element("MaxTemp")

    def __post_init__(self) -> None:
        self.level: Optional[float] = None
        self.hs: Optional[Tuple[int, int]] = None
        self.rgb: Optional[Tuple[int, int, int]] = None
        self.rgbw: Optional[Tuple[int, int, int, int]] = None
        self.color_temp: Optional[int] = None

    @property
    def is_on(self) -> bool:
        """
        Return whether the load is on.
        """

        return bool(self.brightness)

    @property
    def brightness(self) -> Optional[float]:
        """
        Return the brightness of the load, 0-100.
        """

        if self.color_type in (self.ColorType.HSL, self.ColorType.CCT):
            return self.level

        elif self.color_type == self.ColorType.RGB:
            if self.rgb is None:
                return None

            return max(self.rgb) / 255 * 100

        elif self.color_type == self.ColorType.RGBW:
            if self.rgbw is None:
                return None

            return max(self.rgbw) / 255 * 100

        return None
