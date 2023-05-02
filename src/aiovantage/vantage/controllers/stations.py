from aiovantage.config_client.objects import (
    Dimmer,
    DualRelayStation,
    EqCtrl,
    EqUX,
    Keypad,
    ScenePointRelay,
    StationObject,
)
from aiovantage.vantage.controllers.base import BaseController


class StationsController(BaseController[StationObject]):
    item_cls = StationObject
    vantage_types = (Dimmer, DualRelayStation, EqCtrl, EqUX, Keypad, ScenePointRelay)
