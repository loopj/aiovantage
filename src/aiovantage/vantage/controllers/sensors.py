from aiovantage.aci_client.system_objects import (
    AnemoSensor,
    LightSensor,
    OmniSensor,
    Sensor,
    Temperature,
)
from aiovantage.vantage.controllers.base import BaseController


class SensorsController(BaseController[Sensor]):
    item_cls = Sensor
    vantage_types = (AnemoSensor, LightSensor, OmniSensor, Temperature)
    status_types = ("TEMP", "POWER", "CURRENT")
