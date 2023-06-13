from dataclasses import dataclass
from typing import ClassVar, List, Optional

from aiovantage.config_client.xml_dataclass import xml_element

from .object_choice import ObjectChoice


@dataclass
class GetFilterResults:
    interface: ClassVar[str] = "IConfiguration"
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
        objects: List[ObjectChoice] = xml_element("Object", default_factory=list)
