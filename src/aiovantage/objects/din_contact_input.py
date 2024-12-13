"""DIN Contact Input Station."""

from dataclasses import dataclass

from aiovantage.objects.din_station import DINStation


@dataclass
class DINContactInput(DINStation):
    """DIN Contact Input Station."""
