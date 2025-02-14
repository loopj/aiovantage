from aiovantage.objects import SystemObject

from .base import Controller


class ModulesController(Controller[SystemObject]):
    """Modules controller.

    Modules are relay or dimming modules connected to the Vantage system.
    """

    vantage_types = ("Module", "ModuleGen2")
