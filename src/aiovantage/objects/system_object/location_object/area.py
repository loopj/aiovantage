"""Area object."""

from dataclasses import dataclass

from . import LocationObject


@dataclass(kw_only=True)
class Area(LocationObject):
    """Area object."""
