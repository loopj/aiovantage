"""Power profile object."""

from dataclasses import dataclass, field

from .system_object import SystemObject


@dataclass
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

    # Not available in 2.x firmware
    adjust: int | None = field(
        default=None,
        metadata={
            "name": "Adjust",
        },
    )

    # Not available in 2.x firmware
    freq: int | None = field(
        default=None,
        metadata={
            "name": "Freq",
        },
    )

    # Not available in 2.x firmware
    inductive: bool | None = field(
        default=None,
        metadata={
            "name": "Inductive",
        },
    )

    @property
    def is_dimmable(self) -> bool:
        """Return True if loads with this profile are dimmable."""
        return self.max > self.min
