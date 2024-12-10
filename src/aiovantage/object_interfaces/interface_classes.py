"""Field definitions for various 'interface' classes."""

from dataclasses import field


class ShadeOrientation:
    """Shade orientation field support."""

    orientation: str | None = field(
        default=None,
        metadata={
            "name": "ShadeOrientation",
            "type": "Attribute",
        },
    )


class ShadeType:
    """Shade type field support."""

    type: str | None = field(
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
