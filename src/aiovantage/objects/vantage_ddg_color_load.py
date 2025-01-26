"""DMX/DALI Gateway color load object."""

from dataclasses import dataclass

from .rgb_load_base import RGBLoadBase


@dataclass(kw_only=True)
class VantageDDGColorLoad(RGBLoadBase):
    """DMX/DALI Gateway color load object."""

    class Meta:
        name = "Vantage.DDGColorLoad"
