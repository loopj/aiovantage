from aiovantage.objects import Temperature

from .base import Controller


class TemperaturesController(Controller[Temperature]):
    """Temperature device controller.

    Temperature devices are device that measure or control temperature.
    """

    vantage_types = ("Temperature",)
