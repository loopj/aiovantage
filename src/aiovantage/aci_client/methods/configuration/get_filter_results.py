from dataclasses import dataclass, field
from typing import List, Optional

from aiovantage.aci_client.system_objects import ALL_TYPES


@dataclass
class ObjectChoice:
    id: Optional[int] = field(
        default=None,
        metadata={
            "name": "VID",
            "type": "Attribute",
        },
    )
    choice: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "choices": tuple({"name": obj.__name__, "type": obj} for obj in ALL_TYPES),
        },
    )


@dataclass
class GetFilterResults:
    call: Optional["GetFilterResults.Params"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    return_value: Optional["GetFilterResults.Return"] = field(
        default=None,
        metadata={
            "name": "return",
            "type": "Element",
        },
    )

    @dataclass
    class Params:
        count: Optional[int] = field(
            default=50,
            metadata={
                "name": "Count",
                "type": "Element",
                "required": True,
            },
        )
        whole_object: Optional[bool] = field(
            default=True,
            metadata={
                "name": "WholeObject",
                "type": "Element",
                "required": True,
            },
        )
        h_filter: Optional[int] = field(
            default=None,
            metadata={
                "name": "hFilter",
                "type": "Element",
                "required": True,
            },
        )

    @dataclass
    class Return:
        object_value: List[ObjectChoice] = field(
            default_factory=list,
            metadata={
                "name": "Object",
                "type": "Element",
            },
        )
