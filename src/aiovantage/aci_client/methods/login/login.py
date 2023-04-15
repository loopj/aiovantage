from dataclasses import dataclass
from typing import Optional

from aiovantage.aci_client.xml_dataclass import xml_element

@dataclass
class Login:
    call: Optional["Login.Params"] = xml_element("call", default=None)
    return_value: Optional[bool] = xml_element("return", default=None)

    @dataclass
    class Params:
        user: str = xml_element("User")
        password: str = xml_element("Password")