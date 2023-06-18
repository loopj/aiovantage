"""DGColorLoad (RGB load) object."""

from dataclasses import dataclass

from .rgb_load import RGBLoad


@dataclass
class DGColorLoad(RGBLoad):
    """DGColorLoad (RGB load) object."""

    class Meta:
        """Meta class."""

        name = "Vantage.DGColorLoad"
