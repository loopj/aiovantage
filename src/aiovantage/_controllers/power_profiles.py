from aiovantage.objects import PowerProfile

from .base import Controller


class PowerProfilesController(Controller[PowerProfile]):
    """Power profiles controller."""

    vantage_types = ("PowerProfile", "DCPowerProfile", "PWMPowerProfile")
