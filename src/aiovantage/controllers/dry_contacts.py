"""Controller holding and managing Vantage dry contacts."""

from aiovantage.objects import DryContact

from .base import BaseController


class DryContactsController(BaseController[DryContact]):
    """Controller holding and managing Vantage dry contacts."""

    vantage_types = ("DryContact",)
    status_categories = ("BTN",)
