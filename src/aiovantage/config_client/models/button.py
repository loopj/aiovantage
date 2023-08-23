"""Button object."""

from dataclasses import dataclass, field
from typing import Optional

from .system_object import SystemObject
from .types import Parent


@dataclass
class Button(SystemObject):
    """Button object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )

    down_id: int = field(
        metadata={
            "name": "Down",
        }
    )

    up_id: int = field(
        metadata={
            "name": "Up",
        }
    )

    hold_id: int = field(
        metadata={
            "name": "Hold",
        }
    )

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
