from ..models.station import Station
from .base import BaseController


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