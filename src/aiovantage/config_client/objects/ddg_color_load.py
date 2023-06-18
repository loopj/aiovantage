"""DDGColorLoad (RGB load) object."""

from dataclasses import dataclass

from .rgb_load import RGBLoad


@dataclass
class DDGColorLoad(RGBLoad):
    """DDGColorLoad (RGB load) object."""

    class Meta:
        """Meta class."""

        name = "Vantage.DDGColorLoad"
