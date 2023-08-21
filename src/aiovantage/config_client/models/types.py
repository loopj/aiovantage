"""Common types."""

from attr import define, field


@define
class Parent:
    """Parent tag."""

    id: int

    position: int = field(
        metadata={
            "name": "Position",
            "type": "Attribute",
        }
    )
