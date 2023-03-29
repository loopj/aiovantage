from ..models.omni_sensor import OmniSensor
from .base import BaseController


class OmniSensorsController(BaseController[OmniSensor]):
    item_cls = OmniSensor
    vantage_types = ["OmniSensor"]
    event_types = ["TEMP", "POWER", "CURRENT"]
