from dataclasses import dataclass
from typing import Optional

from aiovantage.aci_client.xml_dataclass import xml_element

from ..methods.configuration.close_filter import CloseFilter
from ..methods.configuration.get_filter_results import GetFilterResults
from ..methods.configuration.open_filter import OpenFilter


@dataclass
class IConfiguration:
    open_filter: Optional[OpenFilter] = xml_element("OpenFilter", default=None)
    get_filter_results: Optional[GetFilterResults] = xml_element(
        "GetFilterResults", default=None
    )
    close_filter: Optional[CloseFilter] = xml_element("CloseFilter", default=None)
