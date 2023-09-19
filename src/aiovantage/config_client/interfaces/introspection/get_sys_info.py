"""IIntrospection.GetSysInfo method definition."""

from dataclasses import dataclass, field


@dataclass
class GetSysInfo:
    """IIntrospection.GetSysInfo method definition."""

    interface = "IIntrospection"

    @dataclass
    class SysInfo:
        """SysInfo class."""

        master_number: int = field(metadata={"name": "MasterNumber"})
        serial_number: int = field(metadata={"name": "SerialNumber"})

    @dataclass
    class Return:
        """Method return value."""

        sys_info: "GetSysInfo.SysInfo" = field(metadata={"name": "SysInfo"})

    call = None
    return_value: Return | None = field(
        default=None,
        metadata={
            "name": "return",
        },
    )
