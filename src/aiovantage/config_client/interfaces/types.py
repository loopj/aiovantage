"""ObjectChoice type definition."""

from dataclasses import dataclass, field
from functools import cache
from importlib import import_module
from inspect import getmembers, isclass

from aiovantage.objects import SystemObject


@cache
def get_all_object_choices() -> list[dict[str, str | type[SystemObject]]]:
    """Get all object choices from a module."""
    # Load all SystemObject types into memory
    module = import_module("aiovantage.objects")

    # Build and return choices list
    return [
        {"name": cls.element_name(), "type": cls}
        for _, cls in getmembers(module, isclass)
        if issubclass(cls, SystemObject)
    ]


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
