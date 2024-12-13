"""Contact Input."""

from dataclasses import dataclass

from . import StationObject


@dataclass(kw_only=True)
class ContactInput(StationObject):
    """Contact Input."""
