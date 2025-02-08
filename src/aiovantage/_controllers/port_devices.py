from aiovantage.objects import PortDevice

from .base import BaseController


class PortDevicesController(BaseController[PortDevice]):
    """Port devices controller.

    Port devices are typically "hubs" that communicate with other devices such
    as blinds or lighting systems. It is mostly useful to know about these
    devices so we can set up a proper device hierarchy.
    """

    vantage_types = (
        "Somfy.RS-485_SDN_2_x2E_0_PORT",
        "Somfy.URTSI_2_PORT",
        "Vantage.DmxGateway",
    )
