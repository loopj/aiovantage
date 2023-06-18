"""DCPowerProfile object."""

from dataclasses import dataclass

from .power_profile import PowerProfile


@dataclass
class DCPowerProfile(PowerProfile):
    """DCPowerProfile object."""
