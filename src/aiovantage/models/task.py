"""Task object."""

from dataclasses import dataclass

from aiovantage.models.system_object import SystemObject
from aiovantage.object_interfaces.task import TaskInterface


@dataclass
class Task(SystemObject, TaskInterface):
    """Task object."""
