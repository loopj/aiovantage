"""Parent type."""

from dataclasses import dataclass, field


@dataclass
class Parent:
    """Parent type."""

    vid: int
    position: int = field(metadata={"type": "Attribute"})
