from dataclasses import dataclass
from typing import Optional

from aiovantage.aci_client.xml_dataclass import xml_element

from ..methods.introspection.get_version import GetVersion


@dataclass
class IIntrospection:
    get_version: Optional[GetVersion] = xml_element("GetVersion", default=None)
