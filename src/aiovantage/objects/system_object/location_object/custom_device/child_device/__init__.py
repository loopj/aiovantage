"""Base class for child device objects."""

from dataclasses import dataclass

from aiovantage.objects.types import Parent

from .. import CustomDevice


@dataclass(kw_only=True)
class ChildDevice(CustomDevice):
    """Base class for child device objects."""

    parent: Parent
