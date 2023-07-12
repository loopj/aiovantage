"""Button object."""

from dataclasses import dataclass, field
from typing import Optional

from .child_object import ChildObject
from .system_object import SystemObject


@dataclass
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
