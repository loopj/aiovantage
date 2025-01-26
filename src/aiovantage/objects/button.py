"""Button object."""

from dataclasses import dataclass, field

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

    down: int = field(
        metadata={
            "name": "Down",
        }
    )

    up: int = field(
        metadata={
            "name": "Up",
        }
    )

    hold: int = field(
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

    pressed: bool | None = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    @property
    def text(self) -> str:
        """Return the button text."""
        return f"{self.text1}\n{self.text2}" if self.text2 else self.text1
