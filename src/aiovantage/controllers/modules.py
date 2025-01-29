"""Controller holding and managing Vantage modules."""

from aiovantage.objects import SystemObject

from .base import BaseController


class ModulesController(BaseController[SystemObject]):
    """Controller holding and managing Vantage power modules."""

    vantage_types = ("Module", "ModuleGen2")
