from dataclasses import dataclass
from typing import Optional

from aiovantage.config_client.xml_dataclass import xml_element

@dataclass
class CloseFilter:
    call: Optional[int] = xml_element("call", default=None)
    return_value: Optional[bool] = xml_element("return", default=None)