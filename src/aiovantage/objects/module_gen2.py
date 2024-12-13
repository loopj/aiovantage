"""ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

from dataclasses import dataclass, field

from aiovantage.objects.system_object import SystemObject
from aiovantage.objects.types import Parent


@dataclass
class ModuleGen2(SystemObject):
    """ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
