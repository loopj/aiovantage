"""ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

from attr import define, field

from .system_object import SystemObject
from .types import Parent


@define
class ModuleGen2(SystemObject):
    """ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
