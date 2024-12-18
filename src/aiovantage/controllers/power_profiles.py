"""Controller holding and managing Vantage power profiles."""

from aiovantage.objects import DCPowerProfile, PowerProfile, PWMPowerProfile

from .base import BaseController


class PowerProfilesController(BaseController[PowerProfile]):
    """Controller holding and managing Vantage power profiles."""

    vantage_types = (DCPowerProfile, PowerProfile, PWMPowerProfile)
