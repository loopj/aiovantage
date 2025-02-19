from dataclasses import dataclass, field
from typing import Any

from typing_extensions import override

from aiovantage.command_client import Converter

from .base import Interface, method


class GMemInterface(Interface):
    """GMem object interface."""

    interface_name = "GMem"

    @dataclass
    class Buffer:
        """Response from a GMem fetch operation."""

        type: int = field(metadata={"out": "return"})
        data: bytes = field(metadata={"out": "arg0"})

    # Properties
    value: int | str | bytes | None = None

    # Methods
    @method("Fetch")
    async def fetch(self) -> Buffer:
        """Fetch the contents of the variable.

        Returns:
            The contents of the variable.
        """
        # INVOKE <id> GMem.Fetch
        # -> R:INVOKE <id> <type> GMem.Fetch <buffer> <size>
        return await self.invoke("GMem.Fetch")

    @method("Commit")
    async def commit(self, buffer: bytes) -> None:
        """Set the contents of the variable.

        Args:
            buffer: The contents to set the variable to.
        """
        # INVOKE <id> GMem.Commit <buffer> <size>
        # -> R:INVOKE <id> <rcode> GMem.Commit <buffer> <size>
        await self.invoke("GMem.Commit", buffer)

    # We're using `GETVARIABLE`, `VARIABLE` and `S:VARIABLE` for getting and setting
    # variable values, rather than the GMem object interface, since they are much
    # simpler than working with raw byte arrays.

    async def get_value(self) -> int | str | bytes:
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

        # Parse and return the value
        return _parse_gmem_value(response.args[1])

    async def set_value(self, value: Any) -> None:
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
        await self.command_client.command("VARIABLE", self.vid, value)

    @override
    async def fetch_state(self) -> list[str]:
        return self.update_properties({"value": await self.get_value()})

    @override
    def handle_category_status(self, category: str, *args: str) -> list[str]:
        if category == "VARIABLE":
            # STATUS VARIABLE
            # -> S:VARIABLE <id> <value>
            return self.update_properties({"value": _parse_gmem_value(args[0])})

        return super().handle_category_status(category, *args)


def _parse_gmem_value(value: str) -> int | str | bool:
    # If a "" wrapped string, return as str
    if value.startswith('"') and value.endswith('"'):
        return Converter.deserialize(str, value)

    # If a {} or [] wrapped string, return as bytes
    if (value.startswith("{") and value.endswith("}")) or (
        value.startswith("[") and value.endswith("]")
    ):
        return Converter.deserialize(bytes, value)

    # Otherwise, return as int
    return Converter.deserialize(int, value)
