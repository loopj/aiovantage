"""DCPowerProfile object."""

from attr import define

from .power_profile import PowerProfile


@define
class DCPowerProfile(PowerProfile):
    """DCPowerProfile object."""
