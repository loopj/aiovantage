"""ObjectChoice type definition."""

import inspect
from dataclasses import dataclass, field
from typing import Optional

import aiovantage.config_client.objects
from aiovantage.config_client.xml_dataclass import xml_attribute, xml_tag_from_class

# Get all Vantage object from aiovantage.config_client.objects
ALL_OBJECT_TYPES = [
    item
    for _, item in inspect.getmembers(aiovantage.config_client.objects, inspect.isclass)
]


@dataclass
class ObjectChoice:
    """ObjectChoice type definition.

    Wildcard type that can be used to represent any object type.
    """

    # TODO: Attribute name "id" doesn't conform to snake_case naming style
    id: Optional[int] = xml_attribute("VID", default=None)
    choice: Optional[object] = field(
        default=None,
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
