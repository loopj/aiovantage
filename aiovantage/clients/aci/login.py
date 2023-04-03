from dataclasses import dataclass
from typing import TYPE_CHECKING

from aiovantage.xml_dataclass import from_xml_el, element_field

if TYPE_CHECKING:
    from aiovantage.clients.aci.client import ACIClient


class Login:
    def __init__(self, client: "ACIClient") -> None:
        self.client = client

    @dataclass
    class LoginRequest:
        username: str = element_field("User")
        password: str = element_field("Password")

    @dataclass
    class LoginResponse:
        success: bool

    async def login(self, username: str, password: str) -> LoginResponse:
        response = await self.client.request(
            "ILogin", "Login", self.LoginRequest(username=username, password=password)
        )

        return from_xml_el(response, self.LoginResponse)
