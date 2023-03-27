from typing import Any

from ..models.button import Button
from .base import BaseController


class ButtonsController(BaseController[Button]):
    item_type = Button
    vantage_types = ["Button"]
    event_types = ["BTN"]

    # S:BTN {vid} {PRESS|RELEASE}
    def handle_event(self, obj: Button, args: Any) -> None:
        state = args[0]

        self._logger.debug(
            f"Button state changed for {obj.name} {obj.text} ({obj.id}) to {state}"
        )
