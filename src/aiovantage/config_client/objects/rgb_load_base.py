"""RGB load object."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from aiovantage.config_client.xml_dataclass import xml_element

from .child_object import ChildObject
from .location_object import LocationObject


@dataclass
class RGBLoadBase(LocationObject, ChildObject):
    """RGB load base class."""

    class ColorType(Enum):
        """RGBLoad color types."""

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
        """Declare state attributes in post init."""
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
            self.ColorType.RGB,
            self.ColorType.RGBW,
            self.ColorType.HSL,
        )

    @property
    def is_cct(self) -> bool:
        """Return True if the load is a CCT load."""
        return self.color_type == self.ColorType.CCT
