from dataclasses import dataclass, field

from ..client import ConfigClient


@dataclass
class Login:
    @dataclass
    class Params:
        user: str
        password: str

    call: Params | None = field(default=None, metadata={"name": "call"})
    result: bool | None = field(default=None, metadata={"name": "return"})


@dataclass(kw_only=True)
class ILogin:
    login: Login | None = None


class LoginInterface:
    """Wrapper for the `ILogin` RPC interface."""

    @staticmethod
    async def login(client: ConfigClient, user: str, password: str) -> bool:
        """Login to the ACI service.

        Args:
            client: A config client instance
            user: The username to login with
            password: The password to login with

        Returns:
            True if the login was successful, False otherwise
        """
        return await client.rpc(
            ILogin, Login, Login.Params(user=user, password=password)
        )
