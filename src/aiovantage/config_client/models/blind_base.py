"""Blind base class."""

from dataclasses import dataclass, field
from decimal import Decimal

from .system_object import SystemObject


@dataclass(kw_only=True)
class BlindBase(SystemObject):
    """Blind base class."""

    shade_orientation: str | None = field(default=None, metadata=dict(type="Attribute"))
    shade_type: str | None = field(default=None, metadata=dict(type="Attribute"))

    # State
    position: Decimal | None = field(default=None, metadata={"type": "Ignore"})
