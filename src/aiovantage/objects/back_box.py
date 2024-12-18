"""BackBox object."""

from dataclasses import dataclass

from .location_object import LocationObject


@dataclass
class BackBox(LocationObject):
    """BackBox object."""

    keypad_style: int
