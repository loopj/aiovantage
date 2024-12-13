"""Controller holding and managing Vantage modules."""

from aiovantage.controllers.base import BaseController
from aiovantage.objects import SystemObject


class ModulesController(BaseController[SystemObject]):
    """Controller holding and managing Vantage power modules."""

    vantage_types = ("Module", "ModuleGen2")
