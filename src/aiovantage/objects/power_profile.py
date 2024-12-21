"""Power Profile object."""

from dataclasses import dataclass

from .system_object import SystemObject


@dataclass(kw_only=True)
class PowerProfile(SystemObject):
    """Power Profile object."""

    # Significantly different on 2.x firmware.
    # - Min, Max are ints on 2.x firmware.
    # - DCPowerProfile doesn't inherit from PowerProfile on 2.x firmware.
    # - Can rework this once we drop support for 2.x firmware.

    min: float
    max: float
    adjust: int | None = None
    freq: int | None = None
    inductive: bool | None = None

    @property
    def is_dimmable(self) -> bool:
        """Return True if loads with this profile are dimmable."""
        return self.max > self.min
