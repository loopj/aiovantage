"""Station bus object."""

from dataclasses import dataclass

from .system_object import SystemObject
from .types import Parent


@dataclass(kw_only=True)
class StationBus(SystemObject):
    """Station bus object."""

    parent: Parent
