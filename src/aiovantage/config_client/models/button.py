"""Button object."""

from typing import Optional

from attr import define, field

from .child_object import ChildObject
from .system_object import SystemObject


@define
class Button(ChildObject, SystemObject):
    """Button object."""

    text1: str = field(
        metadata={
            "name": "Text1",
        }
    )

    text2: str = field(
        metadata={
            "name": "Text2",
        }
    )

    up_id: int = field(
        metadata={
            "name": "Up",
        }
    )

    down_id: int = field(
        metadata={
            "name": "Down",
        }
    )

    hold_id: int = field(
        metadata={
            "name": "Hold",
        }
    )

    pressed: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    @property
    def text(self) -> str:
        """Return the button text."""
        return f"{self.text1}\n{self.text2}" if self.text2 else self.text1
