from dataclasses import dataclass, field
from typing import Optional

from aiovantage.aci_client.system_objects import CONCRETE_TYPES, xml_tag_from_class
from aiovantage.aci_client.xml_dataclass import xml_attribute


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
                for cls in CONCRETE_TYPES
            ],
        },
    )