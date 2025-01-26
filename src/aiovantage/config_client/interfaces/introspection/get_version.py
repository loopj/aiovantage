"""IIntrospection.GetVersion method definition."""

from dataclasses import dataclass, field


@dataclass
class GetVersion:
    """IIntrospection.GetVersion method definition."""

    interface = "IIntrospection"

    @dataclass
    class Return:
        """Method return value."""

        kernel: str | None = field(default=None, metadata={"name": "kernel"})
        rootfs: str | None = field(default=None, metadata={"name": "rootfs"})
        app: str | None = field(default=None, metadata={"name": "app"})

    call = None

    result: Return | None = field(
        default=None,
        metadata={
            "name": "return",
        },
    )
