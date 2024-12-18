"""Button object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import ButtonInterface

from .system_object import SystemObject
from .types import Parent


@dataclass
class Button(SystemObject, ButtonInterface):
    """Button object."""

    parent: Parent
    down: int
    up: int
    hold: int
    text1: str
    text2: str

    @property
    def text(self) -> str:
        """Return the button text."""
        return f"{self.text1}\n{self.text2}" if self.text2 else self.text1
