"""Controller holding and managing Vantage temperature sensors."""

from aiovantage.objects import Temperature

from .base import BaseController


class TemperatureSensorsController(BaseController[Temperature]):
    """Controller holding and managing Vantage temperature sensors."""

    vantage_types = ("Temperature",)
