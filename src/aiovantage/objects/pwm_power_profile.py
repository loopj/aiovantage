"""PWM power profile object."""

from dataclasses import dataclass

from .dc_power_profile import DCPowerProfile


@dataclass(kw_only=True)
class PWMPowerProfile(DCPowerProfile):
    """PWM power profile object."""

    inverted: bool = False
