"""ILogin.Login method definition."""

from dataclasses import dataclass, field


@dataclass
class Login:
    """ILogin.Login method definition."""

    # Request:
    # <ILogin>
    #   <Login>
    #     <call>
    #       <User>username</User>
    #       <Password>password</Password>
    #     </call>
    #   </Login>
    # </ILogin>

    interface = "ILogin"

    @dataclass
    class Params:
        """Method parameters."""

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

    call: Params | None = field(default=None)
    return_value: bool | None = field(
        default=None,
        metadata={
            "name": "return",
        },
    )
