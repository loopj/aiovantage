from typing import Any, Sequence, Union

from typing_extensions import override

from aiovantage.aci_client.system_objects import GMem
from aiovantage.vantage.controllers.base import StatefulController

ValueType = Union[bool, int, str]

class GMemController(StatefulController[GMem]):
    item_cls = GMem
    vantage_types = (GMem,)
    status_types = ("VARIABLE",)

    @override
    async def fetch_initial_state(self, id: int) -> None:
        # Fetch initial state of all variables.

        self._update_and_notify(id, value=await self.get_value(id))

    @override
    def handle_state_change(self, id: int, status: str, args: Sequence[str]) -> None:
        # Handle a status update for a variable.

        if status == "VARIABLE":
            # STATUS VARIABLE
            #   -> S:VARIABLE <id> <value>
            value = self._parse_value(id, args[0])
            self._update_and_notify(id, value=value)

    async def get_value(self, id: int) -> Any:
        """
        Get the value of a variable.

        Args:
            id: The variable ID.

        Returns:
            The value of the variable.
        """

        # GETVARIABLE {id}
        #   -> R:GETVARIABLE {id} {value}
        _, value = await self._hc_client.command("GETVARIABLE", id)

        return self._parse_value(id, value)

    async def set_value(self, id: int, value: ValueType) -> None:
        """
        Set the value of a variable.

        Args:
            id: The variable ID.
            value: The value to set.
        """

        # SETVARIABLE {id} {value}
        #   -> R:SETVARIABLE {id} {value}
        await self._hc_client.command("VARIABLE", id, self._encode_value(value))

        # Update the local state
        self._update_and_notify(id, value=value)

    def _encode_value(self, value: ValueType) -> str:
        # Encode the value for the SETVARIABLE command.

        if isinstance(value, bool):
            # Boolean values must be converted to 0 or 1
            return str(int(value))
        elif isinstance(value, str):
            # String values must be wrapped in quotes
            return f'"{value}"'
        else:
            return str(value)

    def _parse_value(self, id: int, value: str) -> ValueType:
        # Parse the value based on the variable type.

        type = GMem.Type(self[id].tag)
        if type == GMem.Type.BOOL:
            return bool(int(value))
        elif type == GMem.Type.NUMBER:
            return int(value)
        elif type == GMem.Type.LEVEL:
            # % = level / 1000
            return int(value)
        elif type == GMem.Type.SECONDS:
            # In milliseconds
            return int(value)
        elif type == GMem.Type.DELAY:
            # In milliseconds
            return int(value)
        elif type == GMem.Type.TEMPERATURE:
            # In 1/1000th of a degree C
            return int(value)
        elif type == GMem.Type.LOAD:
            # Load VID
            return int(value)
        elif type == GMem.Type.TASK:
            # Task VID
            return int(value)
        elif type == GMem.Type.DEVICE_UNITS:
            return int(value)
        else:
            return value
