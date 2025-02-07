from aiovantage.controllers import BaseController
from aiovantage.objects import PowerProfile


class PowerProfilesController(BaseController[PowerProfile]):
    """Power profiles controller."""

    vantage_types = ("PowerProfile", "DCPowerProfile", "PWMPowerProfile")
