"""IConfiguration.OpenFilter method definition."""

from typing import ClassVar, List, Optional

from attr import define, field


@define
class OpenFilter:
    """IConfiguration.OpenFilter method definition."""

    interface: ClassVar[str] = "IConfiguration"
    call: Optional["OpenFilter.Params"] = field(default=None)
    return_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "return",
        },
    )

    @define
    class Params:
        """IConfiguration.OpenFilter method parameters."""

        object_types: Optional[List[str]] = field(
            default=None,
            metadata={
                "name": "ObjectType",
                "wrapper": "Objects",
            },
        )

        xpath: Optional[str] = field(
            default=None,
            metadata={
                "name": "XPath",
            },
        )
