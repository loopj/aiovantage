"""IIntrospection.GetVersion method definition."""

from dataclasses import dataclass, field
from typing import ClassVar, Optional


@dataclass
class GetVersion:
    """IIntrospection.GetVersion method definition."""

    interface: ClassVar[str] = "IIntrospection"
    call = None
    return_value: Optional["GetVersion.Return"] = field(
        default=None, metadata={"name": "return"}
    )

    @dataclass
    class Return:
        """IIntrospection.GetVersion method return value."""

        kernel: Optional[str] = field(default=None)
        rootfs: Optional[str] = field(default=None)
        app: Optional[str] = field(default=None)
