"""Module object."""

from dataclasses import dataclass

from .system_object import SystemObject


@dataclass
class Module(SystemObject):
    """Module object."""
