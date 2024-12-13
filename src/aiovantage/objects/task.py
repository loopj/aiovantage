"""Task object."""

from dataclasses import dataclass

from aiovantage.object_interfaces.task import TaskInterface
from aiovantage.objects.system_object import SystemObject


@dataclass
class Task(SystemObject, TaskInterface):
    """Task object."""
