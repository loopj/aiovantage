"""DDGColorLoad (RGB load) object."""

from dataclasses import dataclass

from .rgb_load_base import RGBLoadBase


@dataclass
class VantageDDGColorLoad(RGBLoadBase):
    """DDGColorLoad (RGB load) object."""

    class Meta:
        name = "Vantage.DDGColorLoad"
