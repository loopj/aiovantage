from aiovantage.controllers.base import BaseController
from aiovantage.models.station import Station


class StationsController(BaseController[Station]):
    item_cls = Station
    vantage_types = (
        "Keypad",
        "Dimmer",
        "ScenePointRelay",
        "DualRelayStation",
        "EqCtrl",
        "EqUX",
    )
