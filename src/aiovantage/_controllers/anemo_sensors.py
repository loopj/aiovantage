from aiovantage.objects import AnemoSensor

from .base import BaseController


class AnemoSensorsController(BaseController[AnemoSensor]):
    """Anemo sensors (wind speed sensors) controller."""

    vantage_types = ("AnemoSensor",)
