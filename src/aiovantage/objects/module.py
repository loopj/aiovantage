"""Module object."""

from dataclasses import dataclass

from .system_object import SystemObject
from .types import Parent


@dataclass
class Module(SystemObject):
    """Module object."""

    parent: Parent
