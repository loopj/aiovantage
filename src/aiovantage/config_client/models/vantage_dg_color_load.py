"""DMX Gateway color load object."""

from dataclasses import dataclass

from .rgb_load_base import RGBLoadBase


@dataclass
class VantageDGColorLoad(RGBLoadBase):
    """DMX Gateway color load object."""

    class Meta:
        name = "Vantage.DGColorLoad"
