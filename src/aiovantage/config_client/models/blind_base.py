"""Blind base class."""

from decimal import Decimal
from typing import Optional

from attr import define, field

from .system_object import SystemObject


@define(kw_only=True, slots=False)
class BlindBase(SystemObject):
    """Blind base class."""

    orientation: Optional[str] = field(
        default=None,
        metadata={
            "name": "ShadeOrientation",
            "type": "Attribute",
        },
    )

    type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ShadeType",
            "type": "Attribute",
        },
    )

    position: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
