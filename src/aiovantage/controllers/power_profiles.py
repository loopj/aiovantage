"""Controller holding and managing Vantage power profiles."""

from aiovantage.controllers.base import BaseController
from aiovantage.models import PowerProfile


class PowerProfilesController(BaseController[PowerProfile]):
    """Controller holding and managing Vantage power profiles."""

    vantage_types = ("PowerProfile", "DCPowerProfile", "PWMPowerProfile")
