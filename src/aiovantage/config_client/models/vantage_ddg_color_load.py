"""DMX/DALI Gateway color load object."""

from attr import define

from .rgb_load_base import RGBLoadBase


@define
class VantageDDGColorLoad(RGBLoadBase):
    """DMX/DALI Gateway color load object."""

    class Meta:
        name = "Vantage.DDGColorLoad"
