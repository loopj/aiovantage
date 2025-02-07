from aiovantage.controllers import BaseController
from aiovantage.objects import Temperature


class TemperatureSensorsController(BaseController[Temperature]):
    """Temperature device controller.

    Temperature devices are device that measure or control temperature.
    """

    vantage_types = ("Temperature",)
