"""Controller holding and managing Vantage port devices."""

from aiovantage.objects import (
    PortDevice,
    SomfyRS485SDN20Port,
    SomfyURTSI2Port,
    VantageDmxGateway,
)

from .base import BaseController


class PortDevicesController(BaseController[PortDevice]):
    """Controller holding and managing Vantage port devices.

    Port devices are typically "hubs" that communicate with other devices such
    as blinds or lighting systems. It is mostly useful to know about these
    devices so we can set up a proper device hierarchy.
    """

    vantage_types = (SomfyRS485SDN20Port, SomfyURTSI2Port, VantageDmxGateway)
