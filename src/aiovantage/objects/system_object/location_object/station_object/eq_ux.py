"""Equinox 41 or Equinox 73 touchscreen."""

from dataclasses import dataclass

from . import StationObject


@dataclass(kw_only=True)
class EqUX(StationObject):
    """Equinox 41 or Equinox 73 touchscreen."""
