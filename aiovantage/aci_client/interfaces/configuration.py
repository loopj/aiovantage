import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from aiovantage.aci_client import ACIClient


# IConfiguration.OpenFilter
@dataclass
class OpenFilterParams:
    objects: Optional[str] = field(
        metadata=dict(
            name="Objects",
        ),
    )
    xpath: Optional[str] = field(
        metadata=dict(
            name="XPath",
        ),
    )


@dataclass
class OpenFilterResponse:
    handle: int


async def open_filter(
    client: "ACIClient", xpath: Optional[str] = None
) -> OpenFilterResponse:
    return await client.request(
        "IConfiguration",
        "OpenFilter",
        params=OpenFilterParams(objects=None, xpath=xpath),
        response_type=OpenFilterResponse,
    )


# IConfiguration.GetFilterResults
@dataclass
class GetFilterResultsParams:
    count: int = field(metadata=dict(name="Count"))
    whole_object: bool = field(metadata=dict(name="WholeObject"))
    handle: int = field(metadata=dict(name="hFilter"))


async def get_filter_results(
    client: "ACIClient", handle: int, count: int = 50, whole_object: bool = True
) -> ET.Element:
    # TODO: Have xsdata parse known objects
    return await client.request(
        "IConfiguration",
        "GetFilterResults",
        params=GetFilterResultsParams(
            count=count, whole_object=whole_object, handle=handle
        ),
    )


# IConfiguration.CloseFilter
@dataclass
class CloseFilterParams:
    handle: int = field(metadata=dict(name="hFilter"))


@dataclass
class CloseFilterResponse:
    success: bool


async def close_filter(client: "ACIClient", handle: int) -> CloseFilterResponse:
    return await client.request(
        "IConfiguration",
        "CloseFilter",
        params=CloseFilterParams(handle=handle),
        response_type=CloseFilterResponse,
    )
