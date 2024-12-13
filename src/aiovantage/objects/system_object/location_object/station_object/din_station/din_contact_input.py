"""DIN Contact Input Station."""

from dataclasses import dataclass

from . import DINStation


@dataclass(kw_only=True)
class DINContactInput(DINStation):
    """DIN Contact Input Station."""
