"""IIntrospection.GetSysInfo method definition."""

from dataclasses import dataclass, field
from typing import ClassVar, Optional


@dataclass
class SysInfo:
    """Partial SysInfo definition."""

    master_number: int = field(metadata={"name": "MasterNumber"})
    serial_number: int = field(metadata={"name": "SerialNumber"})


@dataclass
class GetSysInfo:
    """IIntrospection.GetSysInfo method definition."""

    interface: ClassVar[str] = "IIntrospection"
    call = None
    return_value: Optional["Return"] = field(
        default=None,
        metadata={
            "name": "return",
        },
    )

    @dataclass
    class Return:
        """IIntrospection.GetSysInfo method return value."""

        sys_info: SysInfo = field(metadata={"name": "SysInfo"})
