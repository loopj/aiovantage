"""Controller holding and managing Vantage anemo (wind) sensors."""

from aiovantage.objects import AnemoSensor

from .base import BaseController


class AnemoSensorsController(BaseController[AnemoSensor]):
    """Controller holding and managing Vantage anemo (wind) sensors."""

    vantage_types = ("AnemoSensor",)
