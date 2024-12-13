"""Station bus object."""

from dataclasses import dataclass

from aiovantage.objects.types import Parent

from . import SystemObject


@dataclass(kw_only=True)
class StationBus(SystemObject):
    """Station bus object."""

    parent: Parent
