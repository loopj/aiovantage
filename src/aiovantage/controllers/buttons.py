"""Controller holding and managing Vantage buttons."""

from typing import Any, Dict, Optional, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import ButtonInterface
from aiovantage.config_client.objects import Button

from .base import BaseController


class ButtonsController(BaseController[Button], ButtonInterface):
    """Controller holding and managing Vantage buttons."""

    # Fetch the following object types from Vantage
    vantage_types = ("Button",)

    # Get status updates from "STATUS BTN"
    status_types = ("BTN",)

    @override
    def parse_object_update(
        self, _vid: int, status: str, args: Sequence[str]
    ) -> Optional[Dict[str, Any]]:
        """Handle state changes for a button."""

        if status != "BTN":
            return None

        return {
            "pressed": ButtonInterface.parse_btn_status(args),
        }
