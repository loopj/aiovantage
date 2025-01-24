"""ObjectChoice type definition."""

import inspect
from dataclasses import dataclass, field
from functools import cache
from types import ModuleType
from typing import Any

from aiovantage.config_client import models


def get_all_module_classes(module: ModuleType) -> list[type[Any]]:
    """Get all classes from a module."""
    classes = []
    for _, cls in inspect.getmembers(module, inspect.isclass):
        classes.append(cls)

    return classes


@cache
def get_all_object_choices(module: ModuleType) -> list[dict[str, Any]]:
    """Get all object choices from a module."""
    choices = []
    for cls in get_all_module_classes(module):
        # Get the name of the XML element
        meta = getattr(cls, "Meta", None)
        name = getattr(meta, "name", cls.__qualname__)

        # Add the xsdata choice
        choices.append({"name": name, "type": cls})

    return choices


@dataclass
class ObjectChoice:
    """Wildcard type that can be used to represent any object."""

    id: int = field(
        metadata={
            "name": "VID",
            "type": "Attribute",
        }
    )

    choice: object = field(
        metadata={
            "type": "Wildcard",
            "choices": get_all_object_choices(models),  # type: ignore
        },
    )
