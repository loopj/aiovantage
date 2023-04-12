from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ObjectFilter:
    object_type: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ObjectType",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class OpenFilter:
    call: Optional["OpenFilter.Params"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    return_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "return",
            "type": "Element",
        },
    )

    @dataclass
    class Params:
        objects: Optional[ObjectFilter] = field(
            default=None,
            metadata={
                "name": "Objects",
                "type": "Element",
            },
        )
        xpath: Optional[str] = field(
            default=None,
            metadata={
                "name": "XPath",
                "type": "Element",
            },
        )
