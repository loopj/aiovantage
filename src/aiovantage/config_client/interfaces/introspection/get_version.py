"""IIntrospection.GetVersion method definition."""

from dataclasses import dataclass, field


@dataclass
class GetVersion:
    """IIntrospection.GetVersion method definition."""

    interface = "IIntrospection"

    @dataclass
    class Return:
        """Method return value."""

        kernel: str | None = field(default=None)
        rootfs: str | None = field(default=None)
        app: str | None = field(default=None)

    call = None
    return_value: Return | None = field(
        default=None,
        metadata={
            "name": "return",
        },
    )
