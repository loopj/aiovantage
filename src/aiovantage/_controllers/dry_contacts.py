from aiovantage.controllers import BaseController
from aiovantage.objects import DryContact


class DryContactsController(BaseController[DryContact]):
    """Dry contacts controller."""

    vantage_types = ("DryContact",)
