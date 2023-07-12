"""Controller holding and managing Vantage modules."""

from aiovantage.models import SystemObject

from .base import BaseController


class ModulesController(BaseController[SystemObject]):
    """Controller holding and managing Vantage power modules."""

    vantage_types = ("Module", "ModuleGen2")
    """The Vantage object types that this controller will fetch."""
