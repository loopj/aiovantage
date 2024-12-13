"""PWM power profile object."""

from dataclasses import dataclass

from . import DCPowerProfile


@dataclass(kw_only=True)
class PWMPowerProfile(DCPowerProfile):
    """PWM power profile object."""
