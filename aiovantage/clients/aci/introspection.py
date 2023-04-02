from dataclasses import dataclass
from typing import TYPE_CHECKING

from aiovantage.xml_dataclass import element_field, from_xml_el

if TYPE_CHECKING:
    from aiovantage.clients.aci.client import ACIClient


class Introspection:
    def __init__(self, client: "ACIClient") -> None:
        self.client = client

    @dataclass
    class GetVersionResponse:
        kernel: str = element_field()
        rootfs: str = element_field()
        app: str = element_field()

    # IIntrospection.GetVersion
    async def get_version(self) -> GetVersionResponse:
        response = await self.client.request("IIntrospection", "GetVersion")
        return from_xml_el(response, self.GetVersionResponse)
