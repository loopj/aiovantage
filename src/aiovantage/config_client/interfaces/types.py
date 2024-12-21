"""ObjectChoice type definition."""

from dataclasses import dataclass, field
from functools import cache
from importlib import import_module
from inspect import getmembers, isclass

from aiovantage.objects import SystemObject


@cache
def get_all_object_choices() -> list[dict[str, type[SystemObject]]]:
    """Get all object choices from a module."""
    # Load all SystemObject types into memory
    module = import_module("aiovantage.objects")
    system_object_classes = [
        cls
        for _, cls in getmembers(
            module, lambda m: isclass(m) and issubclass(m, SystemObject)
        )
    ]

    # Build choices list
    choices = []
    for cls in system_object_classes:
        meta = getattr(cls, "Meta", None)
        name = getattr(meta, "name", cls.__qualname__)
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
            "choices": get_all_object_choices(),
        },
    )
