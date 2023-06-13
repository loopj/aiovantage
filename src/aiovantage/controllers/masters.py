from aiovantage.command_client.interfaces import IntrospectionInterface
from aiovantage.config_client.objects import Master
from aiovantage.controllers.base import BaseController


class MastersController(BaseController[Master], IntrospectionInterface):
    # Fetch the following object types from Vantage
    vantage_types = ("Master",)
