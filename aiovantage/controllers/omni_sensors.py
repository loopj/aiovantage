from ..clients.hc import StatusType
from ..models.omni_sensor import OmniSensor
from .base import BaseController


class OmniSensorsController(BaseController[OmniSensor]):
    item_cls = OmniSensor
    vantage_types = ("OmniSensor",)
    status_types = (
        StatusType.TEMP,
        StatusType.POWER,
        StatusType.CURRENT,
    )
