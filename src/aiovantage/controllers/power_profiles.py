"""Controller holding and managing Vantage power profiles."""

from aiovantage.objects import PowerProfile

from .base import BaseController


class PowerProfilesController(BaseController[PowerProfile]):
    """Controller holding and managing Vantage power profiles."""

    vantage_types = ("PowerProfile", "DCPowerProfile", "PWMPowerProfile")
    """The Vantage object types that this controller will fetch."""
