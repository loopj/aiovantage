"""Parent type."""

from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Parent:
    """Parent type."""

    id: int
    position: int = field(metadata={"type": "Attribute"})
