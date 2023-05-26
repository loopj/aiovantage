from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.config_client.objects import GMem
from aiovantage.controllers.base import StatefulController


class GMemController(StatefulController[GMem]):
    # Store objects managed by this controller as GMem instances
    item_cls = GMem

    # Fetch GMem objects from Vantage
    vantage_types = (GMem,)

    # Get status updates from "STATUS VARIABLE"
    status_types = ("VARIABLE",)

    @override
    async def fetch_object_state(self, id: int) -> None:
        # Fetch initial state of all GMem objects.

        state: Dict[str, Any] = {}
        state["value"] = await self.get_value(id)

        self.update_state(id, state)

    @override
    def handle_object_update(self, id: int, status: str, args: Sequence[str]) -> None:
        # Handle state changes for a GMem object.

        state: Dict[str, Any] = {}
        if status == "VARIABLE":
            # STATUS VARIABLE
            # -> S:VARIABLE <id> <value>
            state["value"] = self._parse_value(id, args[0])

        self.update_state(id, state)

    async def get_value(self, id: int) -> GMem.Value:
        """
        Get the value of a variable, and convert it to the correct type.

        Args:
            id: The variable ID.

        Returns:
            The value of the variable, as either a bool, int, or str.
        """

        # GETVARIABLE {id}
        # -> R:GETVARIABLE {id} {value}
        response = await self.command_client.command("GETVARIABLE", id)

        return self._parse_value(id, response.args[1])

    async def set_value(self, id: int, value: GMem.Value) -> None:
        """
        Set the value of a variable.

        Args:
            id: The variable ID.
            value: The value to set, either a bool, int, or str.
        """

        # SETVARIABLE {id} {value}
        # -> R:SETVARIABLE {id} {value}
        await self.command_client.command("VARIABLE", id, self._encode_value(value))

        # Update the local state
        self.update_state(id, {"value": value})

    def _encode_value(self, value: GMem.Value) -> str:
        # Encode the value for the SETVARIABLE command.

        if isinstance(value, bool):
            # Boolean values must be converted to 0 or 1
            return str(int(value))
        elif isinstance(value, str):
            # String values must be wrapped in quotes
            # TODO: Newlines are not allowed, can double quotes be escaped?
            return f'"{value}"'
        else:
            return str(value)

    def _parse_value(self, id: int, value: str) -> GMem.Value:
        # Parse the results of the VARAIBLE command based on the variable type.

        type = GMem.Type(self[id].tag)
        if type == GMem.Type.BOOL:
            return bool(int(value))
        elif type == GMem.Type.TEXT:
            return value
        else:
            return int(value)
