from aiovantage.objects import StationObject

from .base import Controller


class StationsController(Controller[StationObject]):
    """Stations controller.

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
        "IRX2",
        "Keypad",
        "LowVoltageRelayStation",
        "RS232Station",
        "RS485Station",
        "ScenePointRelay",
        "Vantage.DmxDaliGateway",
    )
