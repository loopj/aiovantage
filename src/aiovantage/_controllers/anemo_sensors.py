from aiovantage.controllers import BaseController
from aiovantage.objects import AnemoSensor


class AnemoSensorsController(BaseController[AnemoSensor]):
    """Anemo sensors (wind speed sensors) controller."""

    vantage_types = ("AnemoSensor",)
