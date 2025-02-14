"""DMX/DALI Gateway color load object."""

from dataclasses import dataclass
from enum import Enum

from aiovantage.object_interfaces import (
    ColorTemperatureInterface,
    LoadInterface,
    RGBLoadInterface,
)

from .location_object import LocationObject
from .types import Parent


@dataclass(kw_only=True)
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

    parent: Parent
    color_type: ColorType
    min_temp: int
    max_temp: int
