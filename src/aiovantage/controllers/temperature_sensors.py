"""Temperature device controller."""

from aiovantage.objects import Temperature

from .base import BaseController


class TemperatureSensorsController(BaseController[Temperature]):
    """Temperature device controller.

    Temperature devices are device that measure or control temperature.
    """

    vantage_types = ("Temperature",)
