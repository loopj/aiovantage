from dataclasses import dataclass

from ..rgb_load import RGBLoad


@dataclass
class DDGColorLoad(RGBLoad):
    class Meta:
        name = "Vantage.DDGColorLoad"
