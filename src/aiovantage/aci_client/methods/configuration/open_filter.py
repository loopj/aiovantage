from dataclasses import dataclass
from typing import List, Optional

from aiovantage.aci_client.xml_dataclass import xml_element


@dataclass
class ObjectFilter:
    object_type: List[str] = xml_element("ObjectType")


@dataclass
class OpenFilter:
    call: Optional["OpenFilter.Params"] = xml_element("call", default=None)
    return_value: Optional[int] = xml_element("return", default=None)

    @dataclass
    class Params:
        objects: Optional[ObjectFilter] = xml_element("Objects", default=None)
        xpath: Optional[str] = xml_element("XPath", default=None)
