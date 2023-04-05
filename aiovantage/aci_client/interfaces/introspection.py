from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiovantage.aci_client import ACIClient


@dataclass
class GetVersionResponse:
    kernel: str = field(
        metadata={
            "type": "Element",
        },
    )
    rootfs: str = field(
        metadata={
            "type": "Element",
        },
    )
    app: str = field(
        metadata={
            "type": "Element",
        },
    )


async def get_version(client: "ACIClient") -> GetVersionResponse:
    return await client.request(
        "IIntrospection",
        "GetVersion",
        response_type=GetVersionResponse,
    )
