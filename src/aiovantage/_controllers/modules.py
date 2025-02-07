from aiovantage.controllers import BaseController
from aiovantage.objects import SystemObject


class ModulesController(BaseController[SystemObject]):
    """Modules controller.

    Modules are relay or dimming modules connected to the Vantage system.
    """

    vantage_types = ("Module", "ModuleGen2")
