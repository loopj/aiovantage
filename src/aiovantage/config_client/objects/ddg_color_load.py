"""DDGColorLoad (RGB load) object."""

from dataclasses import dataclass

from .rgb_load_base import RGBLoadBase


@dataclass
class DDGColorLoad(RGBLoadBase):
    """DDGColorLoad (RGB load) object."""

    class Meta:
        """Meta class."""

        name = "Vantage.DDGColorLoad"
