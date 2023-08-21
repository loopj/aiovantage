"""ILogin.Login method definition."""

from typing import ClassVar, Optional

from attr import define, field


@define
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

    @define
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
