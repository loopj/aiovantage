"""Child object mixin."""

from attr import define, field


@define
class ChildObject:
    """Child object mixin."""

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

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )

    @property
    def parent_id(self) -> int:
        """Return the parent id."""
        return self.parent.id

    @property
    def parent_position(self) -> int:
        """Return the parent position."""
        return self.parent.position
