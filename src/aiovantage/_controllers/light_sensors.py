from aiovantage.controllers import BaseController
from aiovantage.objects import LightSensor


class LightSensorsController(BaseController[LightSensor]):
    """Light sensors controller."""

    vantage_types = ("LightSensor",)
