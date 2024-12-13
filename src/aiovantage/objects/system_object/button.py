"""Button object."""

from dataclasses import dataclass

from aiovantage.object_interfaces.button import ButtonInterface
from aiovantage.objects.types import Parent

from . import SystemObject


@dataclass(kw_only=True)
class Button(SystemObject, ButtonInterface):
    """Button object."""

    parent: Parent
    down: int = 0
    up: int = 0
    hold: int = 0
    text_1: str = ""
    text_2: str = ""

    @property
    def text(self) -> str:
        """Return the button text."""
        return f"{self.text_1}\n{self.text_2}" if self.text_2 else self.text_1
