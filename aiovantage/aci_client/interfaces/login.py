from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiovantage.aci_client import ACIClient


@dataclass
class LoginParams:
    username: str = field(
        metadata=dict(
            name="User",
        ),
    )
    password: str = field(
        metadata=dict(
            name="Password",
        ),
    )


@dataclass
class LoginResponse:
    success: bool


async def login(client: "ACIClient", username: str, password: str) -> LoginResponse:
    return await client.request(
        "ILogin",
        "Login",
        params=LoginParams(username=username, password=password),
        response_type=LoginResponse,
    )
