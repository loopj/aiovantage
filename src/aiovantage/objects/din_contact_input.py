"""DIN Contact Input Station."""

from dataclasses import dataclass

from .din_station import DINStation


@dataclass
class DINContactInput(DINStation):
    """DIN Contact Input Station."""
