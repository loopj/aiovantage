from aiovantage.objects import AnemoSensor

from .base import Controller


class AnemoSensorsController(Controller[AnemoSensor]):
    """Anemo sensors (wind speed sensors) controller."""

    vantage_types = ("AnemoSensor",)
