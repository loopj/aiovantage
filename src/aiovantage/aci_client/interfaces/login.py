from dataclasses import dataclass, field
from typing import Optional

from ..methods.login.login import Login


@dataclass
class ILogin:
    login: Optional[Login] = field(
        default=None,
        metadata={
            "name": "Login",
            "type": "Element",
        },
    )
