from dataclasses import dataclass
from typing import ClassVar, List, Optional

from aiovantage.config_client.xml_dataclass import xml_element


@dataclass
class OpenFilter:
    interface: ClassVar[str] = "IConfiguration"
    call: Optional["OpenFilter.Params"] = xml_element("call", default=None)
    return_value: Optional[int] = xml_element("return", default=None)

    @dataclass
    class Filter:
        object_type: List[str] = xml_element("ObjectType")

    @dataclass
    class Params:
        objects: Optional["OpenFilter.Filter"] = xml_element("Objects", default=None)
        xpath: Optional[str] = xml_element("XPath", default=None)
