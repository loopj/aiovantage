"""Button object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces.button import ButtonInterface
from aiovantage.objects.types import Parent

from . import SystemObject


@dataclass
class Button(SystemObject, ButtonInterface):
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

    @property
    def text(self) -> str:
        """Return the button text."""
        return f"{self.text1}\n{self.text2}" if self.text2 else self.text1
