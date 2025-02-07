from aiovantage.controllers import BaseController
from aiovantage.objects import StationObject


class StationsController(BaseController[StationObject]):
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
        "Keypad",
        "LowVoltageRelayStation",
        "RS232Station",
        "RS485Station",
        "ScenePointRelay",
        "Vantage.DmxDaliGateway",
    )
