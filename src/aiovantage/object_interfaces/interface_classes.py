"""Field definitions for various 'interface' classes.

These are effectively 'mixins' to object interfaces which add fields to the
objects that implement them.
"""

from dataclasses import dataclass, field


@dataclass
class ShadeOrientation:
    """Shade orientation field support."""

    shade_orientation: str | None = field(
        default=None,
        metadata={"type": "Attribute"},
    )


@dataclass
class ShadeType:
    """Shade type field support."""

    shade_type: str | None = field(
        default=None,
        metadata={"type": "Attribute"},
    )
