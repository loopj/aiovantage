from aiovantage.controllers import BaseController
from aiovantage.objects import OmniSensor


class OmniSensorsController(BaseController[OmniSensor]):
    """Omni sensors controller.

    Omni sensors are generic sensors objects which specify which methods to use
    when getting or setting data in their object definition, as well as the
    type of data and a conversion formula.
    """

    vantage_types = ("OmniSensor",)
