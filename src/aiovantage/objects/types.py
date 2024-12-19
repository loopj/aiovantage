"""Parent type."""

from dataclasses import dataclass, field


@dataclass
class Parent:
    """Parent type."""

    id: int
    position: int = field(metadata={"type": "Attribute"})
