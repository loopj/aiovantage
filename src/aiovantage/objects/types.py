"""Common types."""

from dataclasses import dataclass, field


@dataclass
class Parent:
    """Parent tag."""

    id: int
    position: int = field(metadata={"type": "Attribute"})
