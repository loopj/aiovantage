"""ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

from dataclasses import dataclass, field

from .system_object import SystemObject
from .types import Parent


@dataclass
class ModuleGen2(SystemObject):
    """ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
