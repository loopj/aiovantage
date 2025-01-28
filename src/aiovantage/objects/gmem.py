"""GMem (variable) object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces import GMemInterface

from .system_object import SystemObject
from .types import Array


@dataclass(kw_only=True)
class GMem(SystemObject, GMemInterface):
    """GMem (variable) object."""

    @dataclass
    class Data(Array):
        fixed: bool = field(default=False, metadata={"type": "Attribute"})

    @dataclass
    class Tag:
        type: str
        object: bool = field(
            default=False, metadata={"name": "object", "type": "Attribute"}
        )

    category: int
    data: Data = field(metadata={"name": "data"})
    persistent: bool = True
    tag: Tag

    @property
    def is_bool(self) -> bool:
        """Return True if GMem is boolean type."""
        return self.tag.type == "bool"

    @property
    def is_str(self) -> bool:
        """Return True if GMem is string type."""
        return self.tag.type == "Text"

    @property
    def is_int(self) -> bool:
        """Return True if GMem is integer type."""
        return self.tag.type in (
            "Delay",
            "DeviceUnits",
            "Level",
            "Load",
            "Number",
            "Seconds",
            "Task",
            "DegC",
        )

    @property
    def is_object_id(self) -> bool:
        """Return True if GMem is a pointer to an object."""
        return self.tag.object

    @property
    def is_fixed(self) -> bool:
        """Return True if GMem is a fixed point number."""
        return self.data.fixed

    async def get_value(self) -> int | str | bool:
        """Get the value of a variable.

        Returns:
            The value of the variable, either a bool, int, or str.
        """
        # GETVARIABLE {id}
        # -> R:GETVARIABLE {id} {value}

        # Make sure we have a command client to send requests with
        if self.command_client is None:
            raise ValueError("The object has no command client to send requests with.")

        # Get the value of the variable
        response = await self.command_client.command("GETVARIABLE", self.vid)
        raw_value = response.args[1]

        return self.parse_value(raw_value)

    async def set_value(self, value: int | str | bool) -> None:
        """Set the value of a variable.

        Args:
            value: The value to set, either a bool, int, or str.
        """
        # VARIABLE {id} {value}
        # -> R:VARIABLE {id} {value}

        # Make sure we have a command client to send requests with
        if self.command_client is None:
            raise ValueError("The object has no command client to send requests with.")

        # Set the value of the variable
        await self.command_client.command(
            "VARIABLE", self.vid, value, force_quotes=True
        )

    def parse_value(self, value: str) -> int | str | bool:
        """Parse the results of a GMem lookup into the expected type."""
        if self.is_bool:
            return bool(int(value))
        if self.is_str:
            return value

        return int(value)
