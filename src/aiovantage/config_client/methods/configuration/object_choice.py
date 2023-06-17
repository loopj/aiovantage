from dataclasses import dataclass, field
from typing import Optional

from aiovantage.config_client.objects import ALL_OBJECT_TYPES
from aiovantage.config_client.xml_dataclass import xml_attribute, xml_tag_from_class


@dataclass
class ObjectChoice:
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
