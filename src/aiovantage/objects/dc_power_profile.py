"""DCPowerProfile object."""

from dataclasses import dataclass

from .power_profile import PowerProfile

# NOTE: Inherits from SystemObject on 2.x firmware, PowerProfile on 3.x firmware.


@dataclass
class DCPowerProfile(PowerProfile):
    """DCPowerProfile object."""
