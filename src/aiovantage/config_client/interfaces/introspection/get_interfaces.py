"""IIntrospection.GetInterfaces method definition."""

from dataclasses import dataclass, field


@dataclass
class Interface:
    """Object interface definition."""

    name: str = field(metadata={"name": "Name"})
    version: str = field(metadata={"name": "Version"})
    id: int = field(metadata={"name": "IID"})


@dataclass
class GetInterfaces:
    """IIntrospection.GetInterfaces method definition."""

    interface = "IIntrospection"
    call = None
    return_value: list[Interface] | None = field(
        default=None,
        metadata={
            "name": "Interface",
            "wrapper": "return",
        },
    )
