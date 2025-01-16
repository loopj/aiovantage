"""Controller holding and managing Vantage modules."""

from aiovantage.objects import Module, ModuleGen2

from .base import BaseController

ModuleTypes = Module | ModuleGen2


class ModulesController(BaseController[ModuleTypes]):
    """Controller holding and managing Vantage power modules."""

    vantage_types = (Module, ModuleGen2)
