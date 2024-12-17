"""BackBox object."""

from dataclasses import dataclass, field

from .location_object import LocationObject


@dataclass
class BackBox(LocationObject):
    """BackBox object."""

    keypad_style: int = field(
        metadata={
            "name": "KeypadStyle",
        }
    )
