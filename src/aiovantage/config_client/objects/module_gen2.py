"""ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

from dataclasses import dataclass

from .child_object import ChildObject
from .system_object import SystemObject


@dataclass
class ModuleGen2(SystemObject, ChildObject):
    """ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""
