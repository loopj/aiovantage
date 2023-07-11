"""Blind base class."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from .system_object import SystemObject


@dataclass
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
