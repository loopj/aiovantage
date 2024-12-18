"""Common types."""

from dataclasses import dataclass, field


@dataclass
class Parent:
    """Parent tag."""

    vid: int
    position: int = field(metadata={"type": "Attribute"})
