from dataclasses import dataclass
from typing import Optional

from aiovantage.config_client.xml_dataclass import xml_element

from ..methods.login.login import Login


@dataclass
class ILogin:
    login: Optional[Login] = xml_element("Login", default=None)
