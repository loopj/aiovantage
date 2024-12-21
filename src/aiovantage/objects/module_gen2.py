"""ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

from dataclasses import dataclass

from .system_object import SystemObject
from .types import Parent


@dataclass(kw_only=True)
class ModuleGen2(SystemObject):
    """ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

    parent: Parent
