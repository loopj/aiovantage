"""DMX/DALI Gateway color load object."""

from dataclasses import dataclass, field
from enum import Enum

from aiovantage.object_interfaces.color_temperature import ColorTemperatureInterface
from aiovantage.object_interfaces.load import LoadInterface
from aiovantage.object_interfaces.rgb_load import RGBLoadInterface
from aiovantage.objects.types import Parent

from . import LocationObject


@dataclass
class VantageDDGColorLoad(
    LocationObject, LoadInterface, RGBLoadInterface, ColorTemperatureInterface
):
    """DMX/DALI Gateway color load object."""

    class Meta:
        name = "Vantage.DDGColorLoad"

    class ColorType(Enum):
        RGB = "RGB"
        RGBW = "RGBW"
        HSL = "HSL"
        HSIC = "HSIC"
        CCT = "CCT"
        COLOR_CHANNEL = "Color Channel"

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )

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