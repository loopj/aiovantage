"""Power profile object."""

from dataclasses import dataclass

from .. import SystemObject


@dataclass(kw_only=True)
class PowerProfile(SystemObject):
    """Power Profile object."""

    # NOTE: adjust, freq, inductive properties are not available in 2.x firmware

    min: float
    max: float
    adjust: int | None = None
    freq: int | None = None
    inductive: bool | None = None

    @property
    def is_dimmable(self) -> bool:
        """Return True if loads with this profile are dimmable."""
        return self.max > self.min
