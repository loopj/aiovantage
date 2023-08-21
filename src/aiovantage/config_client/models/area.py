"""Area object."""

from attr import define

from .location_object import LocationObject


@define
class Area(LocationObject):
    """Area object."""
