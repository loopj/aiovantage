"""Module object."""

from dataclasses import dataclass

from .system_object import SystemObject
from .types import Parent


@dataclass(kw_only=True)
class Module(SystemObject):
    """Module object."""

    parent: Parent
