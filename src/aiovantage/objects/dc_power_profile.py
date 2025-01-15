"""DCPowerProfile object."""

from dataclasses import dataclass

from .power_profile import PowerProfile


@dataclass(kw_only=True)
class DCPowerProfile(PowerProfile):
    """DCPowerProfile object."""
