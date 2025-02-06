"""ILogin.Login method definition."""

from dataclasses import dataclass, field


@dataclass
class Login:
    """ILogin.Login method definition."""

    interface = "ILogin"

    @dataclass
    class Params:
        """Method parameters."""

        user: str
        password: str

    call: Params | None = field(default=None, metadata={"name": "call"})
    result: bool | None = field(default=None, metadata={"name": "return"})


@dataclass
class ILogin:
    """ILogin interface."""

    login: Login | None = None
