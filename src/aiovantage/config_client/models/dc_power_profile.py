"""DCPowerProfile object."""

from attr import define

from .power_profile import PowerProfile

# NOTE: Inherits from SystemObject on 2.x firmware, PowerProfile on 3.x firmware.


@define
class DCPowerProfile(PowerProfile):
    """DCPowerProfile object."""
