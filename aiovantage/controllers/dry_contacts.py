from typing import Any

from ..models.dry_contact import DryContact
from .base import BaseController


class DryContactsController(BaseController[DryContact]):
    item_type = DryContact
    vantage_types = ["DryContact"]
    event_types = ["BTN"]

    # S:BTN {vid} {PRESS|RELEASE}
    def handle_event(self, obj: DryContact, args: Any) -> None:
        state = args[0]

        self._logger.debug(
            f"DryContact state changed for {obj.name} ({obj.id}) to {state}"
        )
