from dataclasses import dataclass, field
from typing import List, Optional

from aiovantage.aci_client.system_objects import ALL_TYPES
from aiovantage.aci_client.xml_dataclass import xml_attribute, xml_element

choices = [
    {
        "name": obj.Meta.name if "Meta" in obj.__dict__ else obj.__name__,  # type: ignore[attr-defined]
        "type": obj,
    }
    for obj in ALL_TYPES
]


@dataclass
class ObjectChoice:
    id: Optional[int] = xml_attribute("VID", default=None)
    choice: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "choices": choices,
        },
    )


@dataclass
class GetFilterResults:
    call: Optional["GetFilterResults.Params"] = xml_element("call", default=None)
    return_value: Optional["GetFilterResults.Return"] = xml_element(
        "return", default=None
    )

    @dataclass
    class Params:
        h_filter: int = xml_element("hFilter")
        count: int = xml_element("Count", default=50)
        whole_object: bool = xml_element("WholeObject", default=True)

    @dataclass
    class Return:
        object_value: List[ObjectChoice] = xml_element("Object", default_factory=list)
