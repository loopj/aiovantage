"""Interface for querying and controlling variables."""

from typing import Sequence, Union

from .base import Interface


class GMemInterface(Interface):
    """Interface for querying and controlling variables."""

    async def get_value(self, vid: int) -> str:
        """Get the value of a variable.

        Args:
            vid: The Vantage ID of the variable.

        Returns:
            The value of the variable, as a raw string.
        """
        # GETVARIABLE {id}
        # -> R:GETVARIABLE {id} {value}
        response = await self.command_client.command("GETVARIABLE", vid)
        value = response.args[1]

        return value

    async def set_value(self, vid: int, value: Union[int, str, bool]) -> None:
        """Set the value of a variable.

        Args:
            vid: The Vantage ID of the variable.
            value: The value to set, either a bool, int, or str.
        """
        # SETVARIABLE {id} {value}
        # -> R:SETVARIABLE {id} {value}
        await self.command_client.command("VARIABLE", vid, value, force_quotes=True)

    @classmethod
    def parse_variable_status(cls, args: Sequence[str]) -> str:
        """Parse a simple 'S:VARIABLE' event.

        Args:
            args: The arguments of the event.

        Returns:
            The level of the load.
        """
        # STATUS VARIABLE
        # -> S:VARIABLE <id> <value>
        return args[0]
