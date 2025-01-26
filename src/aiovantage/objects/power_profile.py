"""Power profile object."""

from dataclasses import dataclass

from .system_object import SystemObject


@dataclass(kw_only=True)
class PowerProfile(SystemObject):
    """Power Profile object."""

    min: float
    max: float

    # Not available in 2.x firmware
    adjust: int | None = None
    freq: int | None = None
    inductive: bool | None = None

    @property
    def is_dimmable(self) -> bool:
        """Return True if loads with this profile are dimmable."""
        return self.max > self.min
