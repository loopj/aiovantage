from aiovantage.config_client.objects import (
    Dimmer,
    DualRelayStation,
    EqCtrl,
    EqUX,
    Keypad,
    ScenePointRelay,
    StationObject,
)
from aiovantage.controllers.base import BaseController


class StationsController(BaseController[StationObject]):
    # Store objects managed by this controller as StationObject instances
    item_cls = StationObject

    # Fetch the following object types from Vantage
    vantage_types = (Dimmer, DualRelayStation, EqCtrl, EqUX, Keypad, ScenePointRelay)
