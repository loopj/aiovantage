import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from aiovantage.clients.aci.interfaces import params_dataclass

if TYPE_CHECKING:
    from aiovantage.clients.aci.client import ACIClient


# IConfiguration.OpenFilter
@params_dataclass
class OpenFilterParams:
    objects: Optional[str] = field(metadata=dict(name="Objects"))
    xpath: Optional[str] = field(metadata=dict(name="XPath"))


@dataclass
class OpenFilterResponse:
    handle: int


async def open_filter(
    client: "ACIClient", xpath: Optional[str] = None
) -> OpenFilterResponse:
    return await client.request(
        "IConfiguration",
        "OpenFilter",
        OpenFilterResponse,
        OpenFilterParams(objects=None, xpath=xpath),
    )


# IConfiguration.GetFilterResults
@params_dataclass
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
        ET.Element,
        GetFilterResultsParams(count=count, whole_object=whole_object, handle=handle),
    )


# IConfiguration.CloseFilter
@params_dataclass
class CloseFilterParams:
    handle: int = field(metadata=dict(name="hFilter"))


@dataclass
class CloseFilterResponse:
    success: bool


async def close_filter(client: "ACIClient", handle: int) -> CloseFilterResponse:
    return await client.request(
        "IConfiguration",
        "CloseFilter",
        CloseFilterResponse,
        CloseFilterParams(handle=handle),
    )
