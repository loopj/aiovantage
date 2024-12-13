"""ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

from dataclasses import dataclass, field

from aiovantage.objects.types import Parent

from . import SystemObject


@dataclass
class ModuleGen2(SystemObject):
    """ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
