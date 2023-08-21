"""ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

from attr import define

from .child_object import ChildObject
from .system_object import SystemObject


@define
class ModuleGen2(ChildObject, SystemObject):
    """ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""
