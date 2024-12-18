"""PWM power profile object."""

from dataclasses import dataclass

from .dc_power_profile import DCPowerProfile


@dataclass
class PWMPowerProfile(DCPowerProfile):
    """PWM power profile object."""
