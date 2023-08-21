"""IIntrospection.GetSysInfo method definition."""

from typing import ClassVar, Optional

from attr import define, field


@define
class SysInfo:
    """Partial SysInfo definition."""

    master_number: int = field(metadata={"name": "MasterNumber"})
    serial_number: int = field(metadata={"name": "SerialNumber"})


@define
class GetSysInfo:
    """IIntrospection.GetSysInfo method definition."""

    interface: ClassVar[str] = "IIntrospection"
    call = None
    return_value: Optional["GetSysInfo.Return"] = field(
        default=None,
        metadata={
            "name": "return",
        },
    )

    @define
    class Return:
        """IIntrospection.GetSysInfo method return value."""

        sys_info: SysInfo = field(metadata={"name": "SysInfo"})
