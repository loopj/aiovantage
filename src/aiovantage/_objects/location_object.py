"""Base class for system objects in an area."""

from dataclasses import dataclass

from .system_object import SystemObject


@dataclass(kw_only=True)
class LocationObject(SystemObject):
    """Base class for system objects in an area."""

    # TODO: Remove the "None" defaults when we drop support for firmware 2.x
    # We have some objects (DryContact, Sensor) inheriting from LocationObject
    # that actually inherit from SystemObject in 2.x firmware

    area: int | None = None
    location: str | None = None
