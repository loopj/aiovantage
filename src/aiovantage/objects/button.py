"""Button object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces import ButtonInterface

from .system_object import SystemObject
from .types import Parent


@dataclass(kw_only=True)
class Button(SystemObject, ButtonInterface):
    """Button object."""

    parent: Parent
    down: int = 0
    up: int = 0
    hold: int = 0
    text1: str
    text2: str
    placement_table: list[int] = field(
        default_factory=list,
        metadata={
            "name": "Place",
            "wrapper": "PlacementTable",
        },
    )
    button_style: int
    led_style: int = field(
        metadata={
            "name": "LEDStyle",
        },
    )

    @property
    def text(self) -> str:
        """Return the button text."""
        return f"{self.text1}\n{self.text2}" if self.text2 else self.text1
