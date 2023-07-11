"""DGColorLoad (RGB load) object."""

from dataclasses import dataclass

from .rgb_load_base import RGBLoadBase


@dataclass
class DGColorLoad(RGBLoadBase):
    """DGColorLoad (RGB load) object."""

    class Meta:
        """Meta class."""

        name = "Vantage.DGColorLoad"
