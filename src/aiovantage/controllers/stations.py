"""Controller holding and managing Vantage stations."""

from aiovantage.config_client.objects import StationObject
from aiovantage.controllers.base import BaseController


class StationsController(BaseController[StationObject]):
    """Controller holding and managing Vantage stations."""

    # Fetch the following object types from Vantage
    vantage_types = (
        "Dimmer",
        "DualRelayStation",
        "EqCtrl",
        "EqUX",
        "Keypad",
        "ScenePointRelay",
    )
