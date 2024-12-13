"""Task object."""

from dataclasses import dataclass

from aiovantage.object_interfaces.task import TaskInterface

from . import SystemObject


@dataclass(kw_only=True)
class Task(SystemObject, TaskInterface):
    """Task object."""
