"""IIntrospection.GetSysInfo method definition."""

from dataclasses import dataclass, field


@dataclass
class SysInfo:
    """Partial SysInfo definition."""

    master_number: int = field(metadata={"name": "MasterNumber"})
    serial_number: int = field(metadata={"name": "SerialNumber"})


@dataclass
class GetSysInfo:
    """IIntrospection.GetSysInfo method definition."""

    @dataclass
    class Return:
        """IIntrospection.GetSysInfo method return value."""

        sys_info: SysInfo = field(metadata={"name": "SysInfo"})

    interface = "IIntrospection"
    call = None
    return_value: Return | None = field(
        default=None,
        metadata={
            "name": "return",
        },
    )
