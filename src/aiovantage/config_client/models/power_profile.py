"""Power profile object."""

from typing import Optional

from attr import define, field

from .system_object import SystemObject


@define
class PowerProfile(SystemObject):
    """Power Profile object."""

    min: float = field(
        metadata={
            "name": "Min",
        }
    )

    max: float = field(
        metadata={
            "name": "Max",
        }
    )

    adjust: Optional[int] = field(
        default=None,
        metadata={
            "name": "Adjust",
        },
    )

    freq: Optional[int] = field(
        default=None,
        metadata={
            "name": "Freq",
        },
    )

    inductive: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Inductive",
        },
    )

    @property
    def is_dimmable(self) -> bool:
        """Return True if loads with this profile are dimmable."""
        return self.max > self.min
