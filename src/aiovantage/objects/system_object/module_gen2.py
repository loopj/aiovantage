"""ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

from dataclasses import dataclass

from aiovantage.objects.types import Parent

from . import SystemObject


@dataclass(kw_only=True)
class ModuleGen2(SystemObject):
    """ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

    parent: Parent
