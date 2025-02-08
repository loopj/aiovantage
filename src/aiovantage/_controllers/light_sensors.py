from aiovantage.objects import LightSensor

from .base import BaseController


class LightSensorsController(BaseController[LightSensor]):
    """Light sensors controller."""

    vantage_types = ("LightSensor",)
