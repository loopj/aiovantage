from datetime import timedelta
from typing import Any, Sequence

from typing_extensions import override

from aiovantage.aci_client.system_objects import GMem
from aiovantage.vantage.controllers.base import StatefulController


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

    async def set_value(self, id: int, value: Any) -> None:
        """
        Set the value of a variable.

        Args:
            id: The variable ID.
            value: The value to set.
        """

        # String values must be wrapped in quotes.
        if isinstance(value, str):
            value = f'"{value}"'

        # SETVARIABLE {id} {value}
        #   -> R:SETVARIABLE {id} {value}
        await self._hc_client.command("VARIABLE", id, value)

    def _parse_value(self, id: int, value: str) -> Any:
        # Parse the value based on the variable type.

        type = GMem.Type(self[id].tag)
        if type == GMem.Type.BOOL:
            return bool(int(value))
        elif type == GMem.Type.NUMBER:
            return int(value)
        elif type == GMem.Type.LEVEL:
            return int(value) / 1000
        elif type == GMem.Type.SECONDS:
            return int(value) / 1000
        elif type == GMem.Type.DELAY:
            return timedelta(milliseconds=int(value))
        elif type == GMem.Type.TEMPERATURE:
            return int(value) / 1000
        elif type == GMem.Type.LOAD:
            return int(value)  # Load VID
        elif type == GMem.Type.TASK:
            return int(value)  # Task VID
        elif type == GMem.Type.DEVICE_UNITS:
            return int(value) / 1000
        else:
            return value
