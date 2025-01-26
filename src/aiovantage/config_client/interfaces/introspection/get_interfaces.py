"""IIntrospection.GetInterfaces method definition."""

from dataclasses import dataclass, field


@dataclass
class GetInterfaces:
    """IIntrospection.GetInterfaces method definition."""

    interface = "IIntrospection"

    @dataclass
    class Interface:
        """Object interface definition."""

        name: str
        version: str
        iid: int = field(metadata={"name": "IID"})

    call = None

    result: list[Interface] | None = field(
        default_factory=list,
        metadata={
            "wrapper": "return",
            "name": "Interface",
            "type": "Element",
        },
    )
