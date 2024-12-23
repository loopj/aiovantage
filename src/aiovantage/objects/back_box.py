"""BackBox object."""

from dataclasses import dataclass

from .location_object import LocationObject


@dataclass(kw_only=True)
class BackBox(LocationObject):
    """BackBox object."""

    keypad_style: int
