from aiovantage.config_client.objects import StationObject
from aiovantage.controllers.base import BaseController


class StationsController(BaseController[StationObject]):
    # Fetch the following object types from Vantage
    vantage_types = (
        "Dimmer",
        "DualRelayStation",
        "EqCtrl",
        "EqUX",
        "Keypad",
        "ScenePointRelay",
    )
