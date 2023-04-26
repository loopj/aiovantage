from typing import Sequence

from typing_extensions import override

from aiovantage.aci_client.system_objects import DryContact
from aiovantage.vantage.controllers.base import StatefulController

# BTN <button vid>
#   -> R:BTN <button vid>
#      R:PRESS <button vid> "EVENT"
#      R:RELEASE <button vid> "EVENT"

# BTNPRESS <button vid>
#   -> R:PRESS <button vid> "EVENT"

# BTNRELEASE <button vid>
#   -> R:RELEASE <button vid> "EVENT"

# STATUS BTN
#   -> R:STATUS BTN
#   -> S:BTN <button vid> <"PRESS" | "RELEASE">

# ADDSTATUS <button vid>
#   -> R:ADDSTATUS <button vid>
#   -> S:STATUS <button vid> Button.GetState <0 | 1>


class DryContactsController(StatefulController[DryContact]):
    item_cls = DryContact
    vantage_types = (DryContact,)

    @override
    async def fetch_initial_state(self, id: int) -> None:
        ...

    @override
    def handle_state_change(self, id: int, status: str, args: Sequence[str]) -> None:
        ...
