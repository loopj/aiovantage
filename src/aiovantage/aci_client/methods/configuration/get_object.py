from dataclasses import dataclass
from typing import List, Optional

from aiovantage.aci_client.xml_dataclass import xml_element

from .object_choice import ObjectChoice

@dataclass
class GetObject:
    call: Optional["GetObject.Params"] = xml_element("call", default=None)
    return_value: Optional["GetObject.Return"] = xml_element("return", default=None)

    @dataclass
    class Params:
        vids: List[int] = xml_element("VID")

    @dataclass
    class Return:
        objects: List[ObjectChoice] = xml_element("Object", default_factory=list)
