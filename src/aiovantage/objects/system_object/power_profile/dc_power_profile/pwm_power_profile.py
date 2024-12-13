"""PWM power profile object."""

from dataclasses import dataclass

from . import DCPowerProfile


@dataclass
class PWMPowerProfile(DCPowerProfile):
    """PWM power profile object."""
