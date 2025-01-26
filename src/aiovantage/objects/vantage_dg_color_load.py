"""DMX Gateway color load object."""

from dataclasses import dataclass

from .rgb_load_base import RGBLoadBase


@dataclass(kw_only=True)
class VantageDGColorLoad(RGBLoadBase):
    """DMX Gateway color load object."""

    class Meta:
        name = "Vantage.DGColorLoad"
