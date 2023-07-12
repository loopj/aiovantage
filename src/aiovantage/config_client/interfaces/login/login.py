"""ILogin.Login method definition."""

from dataclasses import dataclass, field
from typing import ClassVar, Optional


@dataclass
class Login:
    """ILogin.Login method definition."""

    interface: ClassVar[str] = "ILogin"

    call: Optional["Login.Params"] = field(default=None)

    return_value: Optional[bool] = field(
        default=None,
        metadata={
            "name": "return",
        },
    )

    @dataclass
    class Params:
        """ILogin.Login method parameters."""

        user: str = field(
            metadata={
                "name": "User",
            }
        )

        password: str = field(
            metadata={
                "name": "Password",
            }
        )
