"""Field definitions for various 'interface' classes.

These are effectively 'mixins' to object interfaces which add fields to the
objects that implement them.
"""

from dataclasses import field


class ShadeOrientation:
    """Shade orientation field support."""

    shade_orientation: str | None = field(
        default=None,
        metadata={
            "name": "ShadeOrientation",
            "type": "Attribute",
        },
    )


class ShadeType:
    """Shade type field support."""

    shade_type: str | None = field(
        default=None,
        metadata={
            "name": "ShadeType",
            "type": "Attribute",
        },
    )


class WidgetPrecludable:
    """Exclude widget field support."""

    exclude_from_widgets: bool | None = field(
        default=None,
        metadata={
            "name": "ExcludeFromWidgets",
            "type": "Attribute",
        },
    )
