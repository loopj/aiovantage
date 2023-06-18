"""IConfiguration.OpenFilter method definition."""

from dataclasses import dataclass
from typing import ClassVar, List, Optional

from aiovantage.config_client.xml_dataclass import xml_element


@dataclass
class OpenFilter:
    """IConfiguration.OpenFilter method definition."""

    interface: ClassVar[str] = "IConfiguration"
    call: Optional["Params"] = xml_element("call", default=None)
    return_value: Optional[int] = xml_element("return", default=None)

    # @dataclass
    # class Filter:
    #     # TODO: Try using a wrapper
    #     object_type: List[str] = xml_element("ObjectType")

    @dataclass
    class Params:
        """IConfiguration.OpenFilter method parameters."""

        object_types: Optional[List[str]] = xml_element(
            "ObjectType", wrapper="Objects", default=None
        )
        xpath: Optional[str] = xml_element("XPath", default=None)
