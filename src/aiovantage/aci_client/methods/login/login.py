from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Login:
    call: Optional["Login.Params"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    return_value: Optional[bool] = field(
        default=None,
        metadata={
            "name": "return",
            "type": "Element",
        },
    )

    @dataclass
    class Params:
        user: Optional[str] = field(
            default=None,
            metadata={
                "name": "User",
                "type": "Element",
                "required": True,
            },
        )
        password: Optional[str] = field(
            default=None,
            metadata={
                "name": "Password",
                "type": "Element",
                "required": True,
            },
        )
