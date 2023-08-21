"""PWM power profile object."""

from attr import define

from .dc_power_profile import DCPowerProfile


@define
class PWMPowerProfile(DCPowerProfile):
    """PWM power profile object."""
