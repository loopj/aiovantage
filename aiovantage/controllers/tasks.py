import xml.etree.ElementTree as ET
from typing import Any

from ..models.task import Task
from ..utils import get_element_text
from .base import BaseController


class TasksController(BaseController[Task]):
    item_cls = Task
    vantage_types = ["Task"]
    event_types = ["TASK"]

    def from_xml(cls, el: ET.Element) -> "Task":
        return Task(
            id=int(el.attrib["VID"]),
            name=get_element_text(el, "Name"),
            display_name=get_element_text(el, "DName"),
        )

    # S:TASK {vid} {state}
    def handle_event(self, obj: Task, args: Any) -> None:
        state = int(args[0])
        self._logger.debug(f"Task triggered {obj.name} ({obj.id}) to {state}")
