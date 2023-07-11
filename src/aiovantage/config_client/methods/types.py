"""ObjectChoice type definition."""

import inspect
from dataclasses import dataclass, field
from typing import Any, Type

import aiovantage.config_client.objects

# Get all Vantage object from aiovantage.config_client.objects
ALL_OBJECT_TYPES = [
    item
    for _, item in inspect.getmembers(aiovantage.config_client.objects, inspect.isclass)
]


def xml_tag_from_class(cls: Type[Any]) -> str:
    """Get the XML tag name for a class."""
    meta = getattr(cls, "Meta", None)
    name = getattr(meta, "name", cls.__qualname__)

    return name


@dataclass
class ObjectChoice:
    """ObjectChoice type definition.

    Wildcard type that can be used to represent any object type.
    """

    id: int = field(
        metadata={
            "name": "VID",
            "type": "Attribute",
        }
    )

    choice: object = field(
        metadata={
            "type": "Wildcard",
            "choices": [
                {
                    "name": xml_tag_from_class(cls),
                    "type": cls,
                }
                for cls in ALL_OBJECT_TYPES
            ],
        },
    )
