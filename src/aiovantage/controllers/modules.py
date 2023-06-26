"""Controller holding and managing Vantage modules."""

from aiovantage.config_client.objects import SystemObject
from aiovantage.controllers.base import BaseController


class ModulesController(BaseController[SystemObject]):
    """Controller holding and managing Vantage modules."""

    # Fetch the following object types from Vantage
    vantage_types = ("Module", "ModuleGen2")
