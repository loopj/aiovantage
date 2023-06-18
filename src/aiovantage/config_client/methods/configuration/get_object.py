"""IConfiguration.GetObject method definition."""

from dataclasses import dataclass
from typing import ClassVar, List, Optional

from aiovantage.config_client.methods.types import ObjectChoice
from aiovantage.config_client.xml_dataclass import xml_element


@dataclass
class GetObject:
    """IConfiguration.GetObject method definition."""

    interface: ClassVar[str] = "IConfiguration"
    call: Optional["GetObject.Params"] = xml_element("call", default=None)
    return_value: Optional["GetObject.Return"] = xml_element("return", default=None)

    @dataclass
    class Params:
        """IConfiguration.GetObject method parameters."""

        vids: List[int] = xml_element("VID")

    @dataclass
    class Return:
        """IConfiguration.GetObject method return value."""

        objects: List[ObjectChoice] = xml_element("Object", default_factory=list)
