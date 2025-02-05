"""Field definitions for various "interface provided" object fields."""

from dataclasses import dataclass, field


@dataclass(kw_only=True)
class ShadeOrientation:
    """Shade orientation field support."""

    shade_orientation: str | None = field(
        default=None,
        repr=False,
        metadata={"type": "Attribute"},
    )


@dataclass(kw_only=True)
class ShadeType:
    """Shade type field support."""

    shade_type: str | None = field(
        default=None,
        repr=False,
        metadata={"type": "Attribute"},
    )
