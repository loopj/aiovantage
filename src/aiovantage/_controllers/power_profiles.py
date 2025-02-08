from aiovantage.objects import PowerProfile

from .base import BaseController


class PowerProfilesController(BaseController[PowerProfile]):
    """Power profiles controller."""

    vantage_types = ("PowerProfile", "DCPowerProfile", "PWMPowerProfile")
