"""Controller holding and managing Vantage omni sensors."""

from aiovantage.objects.omni_sensor import OmniSensor

from .base import BaseController


class OmniSensorsController(BaseController[OmniSensor]):
    """Controller holding and managing Vantage omni sensors.

    Omni sensors are generic sensors objects which specify which methods to use
    when getting or setting data in their object definition, as well as the
    type of data and a conversion formula.
    """

    vantage_types = ("OmniSensor",)
