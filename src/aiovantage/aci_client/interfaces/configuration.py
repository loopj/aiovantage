from dataclasses import dataclass, field
from typing import Optional

from ..methods.configuration.close_filter import CloseFilter
from ..methods.configuration.get_filter_results import GetFilterResults
from ..methods.configuration.open_filter import OpenFilter


@dataclass
class IConfiguration:
    open_filter: Optional[OpenFilter] = field(
        default=None,
        metadata={
            "name": "OpenFilter",
            "type": "Element",
        },
    )
    get_filter_results: Optional[GetFilterResults] = field(
        default=None,
        metadata={
            "name": "GetFilterResults",
            "type": "Element",
        },
    )
    close_filter: Optional[CloseFilter] = field(
        default=None,
        metadata={
            "name": "CloseFilter",
            "type": "Element",
        },
    )
