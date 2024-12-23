"""Controller holding and managing Vantage modules."""

from aiovantage.objects import Module, ModuleGen2

from .base import BaseController

# The various "module" object types don't all inherit from the same base class,
# so for typing purposes we'll export a union of all the types.
ModuleTypes = Module | ModuleGen2


class ModulesController(BaseController[ModuleTypes]):
    """Controller holding and managing Vantage power modules."""

    vantage_types = (Module, ModuleGen2)
