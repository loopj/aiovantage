"""Base class for custom device (driver provided) objects."""

from dataclasses import dataclass

from .location_object import LocationObject


@dataclass(kw_only=True)
class CustomDevice(LocationObject):
    """Base class for custom device (driver provided) objects."""

    version: float
    device_category: str = ""
    log: str = "None"
