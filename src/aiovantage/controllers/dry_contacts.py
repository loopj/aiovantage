"""Controller holding and managing Vantage dry contacts."""

from typing import Any, Dict, Optional, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import ButtonInterface
from aiovantage.config_client.objects import DryContact

from .base import BaseController


class DryContactsController(BaseController[DryContact], ButtonInterface):
    """Controller holding and managing Vantage dry contacts."""

    # Fetch the following object types from Vantage
    vantage_types = ("DryContact",)

    # Get status updates from "STATUS BTN"
    status_types = ("BTN",)

    @override
    def parse_object_update(
        self, _vid: int, status: str, args: Sequence[str]
    ) -> Optional[Dict[str, Any]]:
        """Handle state changes for a dry contact."""

        if status != "BTN":
            return None

        return {
            "triggered": ButtonInterface.parse_btn_status(args),
        }
