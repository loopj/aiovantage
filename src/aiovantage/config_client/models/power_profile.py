"""Power profile object."""

from dataclasses import dataclass

from .system_object import SystemObject


@dataclass
class PowerProfile(SystemObject):
    """Power Profile object."""

    # Adjust, Freq, Inductive, not available in 2.x firmware

    min: float
    max: float
    adjust: int | None = None
    freq: int | None = None
    inductive: bool | None = None

    @property
    def is_dimmable(self) -> bool:
        """Return True if loads with this profile are dimmable."""
        return self.max > self.min
