"""Controller holding and managing Vantage stations."""

from aiovantage.objects import StationObject

from .base import BaseController


class StationsController(BaseController[StationObject]):
    """Controller holding and managing Vantage stations.

    Stations typically represent keypads or remote relays. It is mostly useful
    to know about these devices so we can set up a proper device hierarchy.
    """

    vantage_types = (
        "ContactInput",
        "Dimmer",
        "DINContactInput",
        "DINHighVoltageRelayStation",
        "DINLowVoltageRelayStation",
        "DualRelayStation",
        "EqCtrl",
        "EqUX",
        "HighVoltageRelayStation",
        "Keypad",
        "LowVoltageRelayStation",
        "RS232Station",
        "RS485Station",
        "ScenePointRelay",
        "Vantage.DmxDaliGateway",
    )
    """The Vantage object types that this controller will fetch."""
