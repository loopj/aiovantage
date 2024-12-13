"""DIN Contact Input Station."""

from dataclasses import dataclass

from . import DINStation


@dataclass
class DINContactInput(DINStation):
    """DIN Contact Input Station."""
