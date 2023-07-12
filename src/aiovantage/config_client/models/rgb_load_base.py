"""RGB load object."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Tuple

from .child_object import ChildObject
from .location_object import LocationObject


@dataclass
class RGBLoadBase(ChildObject, LocationObject):
    """RGB load base class."""

    class ColorType(Enum):
        RGB = "RGB"
        RGBW = "RGBW"
        HSL = "HSL"
        HSIC = "HSIC"
        CCT = "CCT"
        COLOR_CHANNEL = "Color Channel"

    color_type: ColorType = field(
        metadata={
            "name": "ColorType",
        }
    )

    min_temp: int = field(
        metadata={
            "name": "MinTemp",
        }
    )

    max_temp: int = field(
        metadata={
            "name": "MaxTemp",
        }
    )

    hsl: Optional[Tuple[int, int, int]] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    rgb: Optional[Tuple[int, int, int]] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    rgbw: Optional[Tuple[int, int, int, int]] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    level: Optional[int] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    color_temp: Optional[int] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

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
