"""Dry contacts controller."""

from aiovantage.objects import DryContact

from .base import BaseController


class DryContactsController(BaseController[DryContact]):
    """Dry contacts controller."""

    vantage_types = ("DryContact",)
