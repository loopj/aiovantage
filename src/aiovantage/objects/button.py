"""Button object."""

from dataclasses import dataclass, field

from .system_object import SystemObject
from .types import Parent


@dataclass(kw_only=True)
class Button(SystemObject):
    """Button object."""

    parent: Parent
    down: int
    up: int
    hold: int
    text1: str
    text2: str

    # State
    pressed: bool | None = field(default=None, metadata={"type": "Ignore"})

    @property
    def text(self) -> str:
        """Return the button text."""
        return f"{self.text1}\n{self.text2}" if self.text2 else self.text1
