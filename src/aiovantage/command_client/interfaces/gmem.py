from typing import Sequence, Union

from .base import Interface


class GMemInterface(Interface):
    async def get_value(self, id: int) -> str:
        """
        Get the value of a variable.

        Args:
            id: The variable ID.

        Returns:
            The value of the variable, as a raw string.
        """

        # GETVARIABLE {id}
        # -> R:GETVARIABLE {id} {value}
        response = await self.command_client.command("GETVARIABLE", id)
        value = response.args[1]

        return value

    async def set_value(self, id: int, value: Union[int, str, bool]) -> None:
        """
        Set the value of a variable.

        Args:
            id: The variable ID.
            value: The value to set, either a bool, int, or str.
        """

        # SETVARIABLE {id} {value}
        # -> R:SETVARIABLE {id} {value}
        await self.command_client.command("VARIABLE", id, value, force_quotes=True)

    @classmethod
    def parse_variable_status(cls, args: Sequence[str]) -> str:
        """
        Parse a simple "S:VARIABLE" event.

        Args:
            args: The arguments of the event.

        Returns:
            The level of the load.
        """

        # STATUS VARIABLE
        # -> S:VARIABLE <id> <value>
        return args[0]
