from aiovantage.objects import OmniSensor

from .base import Controller


class OmniSensorsController(Controller[OmniSensor]):
    """Omni sensors controller.

    Omni sensors are generic sensors objects which specify which methods to use
    when getting or setting data in their object definition, as well as the
    type of data and a conversion formula.
    """

    vantage_types = ("OmniSensor",)
