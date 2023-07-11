"""Child object mixin."""

from dataclasses import dataclass

from aiovantage.config_client.xml_dataclass import xml_attribute, xml_element, xml_text


@dataclass
class ChildObject:
    """Child object mixin."""

    @dataclass
    class Parent:
        """Parent tag."""

        id: int = xml_text()
        position: int = xml_attribute("Position")

    parent: Parent = xml_element("Parent")

    @property
    def parent_id(self) -> int:
        """Return the parent id."""
        return self.parent.id

    @property
    def parent_position(self) -> int:
        """Return the parent position."""
        return self.parent.position
