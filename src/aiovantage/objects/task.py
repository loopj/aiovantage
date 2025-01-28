"""Task object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import TaskInterface

from .system_object import SystemObject


@dataclass(kw_only=True)
class Task(SystemObject, TaskInterface):
    """Task object."""
