from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiovantage.clients.aci.client import ACIClient


@dataclass
class GetVersionResponse:
    kernel: str = field(metadata=dict(type="Element"))
    rootfs: str = field(metadata=dict(type="Element"))
    app: str = field(metadata=dict(type="Element"))


async def get_version(client: "ACIClient") -> GetVersionResponse:
    return await client.request(
        "IIntrospection",
        "GetVersion",
        GetVersionResponse,
    )
