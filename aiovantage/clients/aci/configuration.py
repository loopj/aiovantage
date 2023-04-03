import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import TYPE_CHECKING, AsyncIterator, Iterable, Optional, Union

from aiovantage.xml_dataclass import element_field, from_xml_el

if TYPE_CHECKING:
    from aiovantage.clients.aci.client import ACIClient


class Configuration:
    def __init__(self, client: "ACIClient") -> None:
        self.client = client

    # IConfiguration.OpenFilter
    @dataclass
    class OpenFilterRequest:
        objects: Optional[str] = element_field(name="Objects")
        xpath: Optional[str] = element_field(name="XPath")

    @dataclass
    class OpenFilterResponse:
        handle: int

    async def open_filter(self, xpath: Optional[str] = None) -> OpenFilterResponse:
        response = await self.client.request(
            "IConfiguration",
            "OpenFilter",
            self.OpenFilterRequest(objects=None, xpath=xpath),
        )
        return from_xml_el(response, self.OpenFilterResponse)

    # IConfiguration.GetFilterResults
    @dataclass
    class GetFilterResultsRequest:
        count: int = element_field(name="Count")
        whole_object: bool = element_field(name="WholeObject")
        handle: int = element_field(name="hFilter")

    @dataclass
    class GetFilterResultsResponse:
        objects: list[ET.Element] = element_field(
            name="Object", default=None
        )

    async def get_filter_results(
        self, handle: int, count: int = 50, whole_object: bool = True
    ) -> ET.Element:
        response = await self.client.request(
            "IConfiguration",
            "GetFilterResults",
            self.GetFilterResultsRequest(
                count=count, whole_object=whole_object, handle=handle
            ),
        )
        return response

    # IConfiguration.CloseFilter
    @dataclass
    class CloseFilterRequest:
        handle: int = element_field(name="hFilter")

    @dataclass
    class CloseFilterResponse:
        success: bool

    async def close_filter(self, handle: int) -> CloseFilterResponse:
        response = await self.client.request(
            "IConfiguration",
            "CloseFilter",
            self.CloseFilterRequest(handle=handle),
        )
        return from_xml_el(response, self.CloseFilterResponse)

    # Convenience method that combines OpenFilter, GetFilterResults, and CloseFilter
    async def get_objects(
        self,
        object_types: Union[Iterable[str], str, None] = None,
        per_page: int = 50,
        whole_object: bool = True,
    ) -> AsyncIterator[ET.Element]:
        # Build the strange XPath string
        xpath = None
        if object_types is not None:
            if isinstance(object_types, str):
                object_types = [object_types]
            xpath = " or ".join([f"/{str}" for str in object_types])

        # Get the handle
        open_response = await self.open_filter(xpath)

        # Get the paginated results, yielding each object
        while True:
            response = await self.get_filter_results(open_response.handle, per_page, whole_object)
            if not response:
                break

            for object in response:
                if len(object) == 1:
                    # TODO: Have xsdata parse known objects
                    yield object[0]

        # Close the filter
        await self.close_filter(open_response.handle)
