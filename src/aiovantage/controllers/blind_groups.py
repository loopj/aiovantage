"""Controller holding and managing Vantage blind groups."""

from aiovantage.objects import BlindGroup, SomfyRS485GroupChild, SomfyURTSI2GroupChild

from .base import BaseController

# The various "blind group" object types don't all inherit from the same base class,
# so for typing purposes we'll use a union of all the types.
BlindGroupTypes = BlindGroup | SomfyRS485GroupChild | SomfyURTSI2GroupChild


class BlindGroupsController(BaseController[BlindGroupTypes]):
    """Controller holding and managing Vantage blind groups."""

    vantage_types = (BlindGroup, SomfyRS485GroupChild, SomfyURTSI2GroupChild)
