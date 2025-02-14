from aiovantage.objects import LightSensor

from .base import Controller


class LightSensorsController(Controller[LightSensor]):
    """Light sensors controller."""

    vantage_types = ("LightSensor",)
