"""IIntrospection.GetVersion method definition."""

from typing import ClassVar, Optional

from attr import define, field


@define
class GetVersion:
    """IIntrospection.GetVersion method definition."""

    interface: ClassVar[str] = "IIntrospection"
    call = None
    return_value: Optional["GetVersion.Return"] = field(
        default=None,
        metadata={
            "name": "return",
        },
    )

    @define
    class Return:
        """IIntrospection.GetVersion method return value."""

        kernel: Optional[str] = field(default=None)
        rootfs: Optional[str] = field(default=None)
        app: Optional[str] = field(default=None)
