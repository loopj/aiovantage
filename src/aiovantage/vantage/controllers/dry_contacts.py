from typing import Sequence

from typing_extensions import override

from aiovantage.config_client.objects import DryContact
from aiovantage.vantage.controllers.base import StatefulController

# BTN <button vid>
#   -> R:BTN <button vid>
#      R:PRESS <button vid> "EVENT"
#      R:RELEASE <button vid> "EVENT"

# BTNPRESS <button vid>
# -> R:PRESS <button vid> "EVENT"

# BTNRELEASE <button vid>
# -> R:RELEASE <button vid> "EVENT"

# ADDSTATUS <button vid>
# -> R:ADDSTATUS <button vid>
# -> S:STATUS <button vid> Button.GetState <0 | 1>

class DryContactsController(StatefulController[DryContact]):
    # Store objects managed by this controller as DryContact instances
    item_cls = DryContact

    # Fetch DryContact objects from Vantage
    vantage_types = (DryContact,)

    # Get status updates from "STATUS BTN"
    status_types = ("BTN",)

    @override
    async def fetch_initial_state(self, id: int) -> None:
        # Fetch initial state of all DryContact objects.

        self.update_state(id, {"state": await self.get_state(id)})

    @override
    def handle_state_change(self, id: int, status: str, args: Sequence[str]) -> None:
        # Handle a status update for a Load.

        if status == "BTN":
            # STATUS BTN
            # -> S:BTN <id> <PRESS | RELEASE>
            # state = args[0]
            # self.update_state(id, {"level": level})
            pass

    async def get_state(self, id: int) -> str:
        # INVOKE <id> Button.GetState
        # -> R:INVOKE <id> <Up|Down> Button.GetState
        response = await self.command_client.invoke(id, "Button.GetState")
        state = response[1]

        return state