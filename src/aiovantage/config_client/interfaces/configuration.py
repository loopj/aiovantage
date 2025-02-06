"""IConfiguration interfaces."""

from dataclasses import dataclass, field


@dataclass
class Object:
    """Wildcard type that can be used to represent any object."""

    vid: int = field(metadata={"name": "VID", "type": "Attribute"})
    obj: object = field(metadata={"type": "Wildcard"})


@dataclass
class OpenFilter:
    """IConfiguration.OpenFilter method definition."""

    interface = "IConfiguration"

    @dataclass
    class Params:
        """Method parameters."""

        object_types: list[str] | None = field(
            default=None,
            metadata={"wrapper": "Objects", "name": "ObjectType", "type": "Element"},
        )
        xpath: str | None = field(default=None, metadata={"name": "XPath"})

    call: Params | None = field(default=None, metadata={"name": "call"})
    result: int | None = field(default=None, metadata={"name": "return"})


@dataclass
class GetFilterResults:
    """IConfiguration.GetFilterResults method definition."""

    interface = "IConfiguration"

    @dataclass
    class Params:
        """Method parameters."""

        h_filter: int = field(metadata={"name": "hFilter"})
        count: int = 50
        whole_object: bool = True

    @dataclass
    class Object:
        """Wildcard type that can be used to represent any object."""

        vid: int = field(metadata={"name": "VID", "type": "Attribute"})
        obj: object = field(metadata={"type": "Wildcard"})

    call: Params | None = field(default=None, metadata={"name": "call"})
    result: list[Object] | None = field(
        default=None,
        metadata={"wrapper": "return", "name": "Object", "type": "Element"},
    )


@dataclass
class CloseFilter:
    """IConfiguration.CloseFilter method definition."""

    interface = "IConfiguration"

    call: int | None = field(default=None, metadata={"name": "call"})
    result: bool | None = field(default=None, metadata={"name": "return"})


@dataclass
class GetObject:
    """IConfiguration.GetObject method definition."""

    interface = "IConfiguration"

    call: list[int] | None = field(
        default=None, metadata={"wrapper": "call", "name": "VID", "type": "Element"}
    )

    result: list[Object] | None = field(
        default=None,
        metadata={"wrapper": "return", "name": "Object", "type": "Element"},
    )


@dataclass
class IConfiguration:
    """IConfiguration interface."""

    open_filter: OpenFilter | None = None
    get_filter_results: GetFilterResults | None = None
    close_filter: CloseFilter | None = None
    get_object: GetObject | None = None
