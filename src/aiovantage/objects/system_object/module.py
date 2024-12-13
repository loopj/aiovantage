"""Module object."""

from dataclasses import dataclass

from aiovantage.objects.types import Parent

from . import SystemObject


@dataclass(kw_only=True)
class Module(SystemObject):
    """Module object."""

    parent: Parent
