"""Controller holding and managing Vantage light sensors."""

from aiovantage.objects import LightSensor

from .base import BaseController


class LightSensorsController(BaseController[LightSensor]):
    """Controller holding and managing Vantage light sensors."""

    vantage_types = ("LightSensor",)
