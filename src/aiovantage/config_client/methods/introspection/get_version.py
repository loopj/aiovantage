from dataclasses import dataclass
from typing import Optional

from aiovantage.config_client.xml_dataclass import xml_element

@dataclass
class GetVersion:
    call: Optional[object] = None
    return_value: Optional["GetVersion.Return"] = xml_element("return", default=None)

    @dataclass
    class Return:
        kernel: Optional[str] = xml_element("kernel", default=None)
        rootfs: Optional[str] = xml_element("rootfs", default=None)
        app: Optional[str] = xml_element("app", default=None)
