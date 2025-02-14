from aiovantage.objects import DryContact

from .base import Controller


class DryContactsController(Controller[DryContact]):
    """Dry contacts controller."""

    vantage_types = ("DryContact",)
