"""Controller holding and managing Vantage modules."""

from aiovantage.config_client.models import SystemObject
from aiovantage.controllers.base import BaseController


class ModulesController(BaseController[SystemObject]):
    """Controller holding and managing Vantage power modules."""

    vantage_types = ("Module", "ModuleGen2")
    """The Vantage object types that this controller will fetch."""
