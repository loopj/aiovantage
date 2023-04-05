from aiovantage.hc_client import StatusType
from aiovantage.controllers.base import BaseController
from aiovantage.models.omni_sensor import OmniSensor


class OmniSensorsController(BaseController[OmniSensor]):
    item_cls = OmniSensor
    vantage_types = ("OmniSensor",)
    status_types = (
        StatusType.TEMP,
        StatusType.POWER,
        StatusType.CURRENT,
    )
