"""Controller holding and managing Vantage port devices."""

from aiovantage.models import PortDevice

from .base import BaseController


class PortDevicesController(BaseController[PortDevice]):
    """Controller holding and managing Vantage port devices."""

    vantage_types = ("Somfy.URTSI_2_PORT", "Vantage.DmxGateway")
    """The Vantage object types that this controller will fetch."""
