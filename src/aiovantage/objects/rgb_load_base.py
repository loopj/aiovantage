"""RGB load object."""

from dataclasses import dataclass, field
from enum import Enum

from .location_object import LocationObject
from .types import Parent


@dataclass(kw_only=True)
class RGBLoadBase(LocationObject):
    """RGB load base class."""

    class ColorType(Enum):
        RGB = "RGB"
        RGBW = "RGBW"
        HSL = "HSL"
        HSIC = "HSIC"
        CCT = "CCT"
        COLOR_CHANNEL = "Color Channel"

    parent: Parent
    color_type: ColorType
    min_temp: int
    max_temp: int

    # State
    hsl: tuple[int, int, int] | None = field(default=None, metadata={"type": "Ignore"})
    rgb: tuple[int, int, int] | None = field(default=None, metadata={"type": "Ignore"})
    rgbw: tuple[int, int, int, int] | None = field(
        default=None, metadata={"type": "Ignore"}
    )
    level: int | None = field(default=None, metadata={"type": "Ignore"})
    color_temp: int | None = field(default=None, metadata={"type": "Ignore"})

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
