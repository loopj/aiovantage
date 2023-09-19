"""IIntrospection.GetVersion method definition."""

from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class GetVersion:
    """IIntrospection.GetVersion method definition."""

    @dataclass
    class Return:
        """IIntrospection.GetVersion method return value."""

        kernel: str | None = field(default=None)
        rootfs: str | None = field(default=None)
        app: str | None = field(default=None)

    interface: ClassVar[str] = "IIntrospection"
    call = None
    return_value: Return | None = field(
        default=None,
        metadata={
            "name": "return",
        },
    )
