from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from aiovantage.clients.aci.interfaces import params_dataclass

if TYPE_CHECKING:
    from aiovantage.clients.aci.client import ACIClient


@params_dataclass
class LoginParams:
    username: str = field(metadata=dict(name="User"))
    password: str = field(metadata=dict(name="Password"))


@dataclass
class LoginResponse:
    success: bool


async def login(client: "ACIClient", username: str, password: str) -> LoginResponse:
    return await client.request(
        "ILogin",
        "Login",
        LoginResponse,
        LoginParams(username=username, password=password),
    )
