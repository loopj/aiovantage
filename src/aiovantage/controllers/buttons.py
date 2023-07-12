"""Controller holding and managing Vantage buttons."""

from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import ButtonInterface
from aiovantage.config_client.models import Button

from .base import BaseController, State


class ButtonsController(BaseController[Button], ButtonInterface):
    """Controller holding and managing Vantage buttons."""

    vantage_types = ("Button",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("BTN",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    def parse_object_update(self, _vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for a button."""
        if status != "BTN":
            return None

        return {
            "pressed": ButtonInterface.parse_btn_status(args),
        }
