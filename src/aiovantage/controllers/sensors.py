from aiovantage.aci_client.system_objects import SENSOR_TYPES, Sensor
from aiovantage.controllers.base import BaseController
from aiovantage.hc_client import StatusType


class SensorsController(BaseController[Sensor]):
    item_cls = Sensor
    vantage_types = (type.__name__ for type in SENSOR_TYPES)
    status_types = (
        StatusType.TEMP,
        StatusType.POWER,
        StatusType.CURRENT,
    )
