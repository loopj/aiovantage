from dataclasses import dataclass

from .rgb_load import RGBLoad


@dataclass
class DGColorLoad(RGBLoad):
    class Meta:
        name = "Vantage.DGColorLoad"
