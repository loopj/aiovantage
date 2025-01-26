"""IIntrospection.GetSysInfo method definition."""

from dataclasses import dataclass, field


@dataclass
class GetSysInfo:
    """IIntrospection.GetSysInfo method definition."""

    interface = "IIntrospection"

    @dataclass
    class SysInfo:
        """SysInfo class."""

        master_number: int
        serial_number: int

    @dataclass
    class Return:
        """Method return value."""

        sys_info: "GetSysInfo.SysInfo"

    call = None

    result: Return | None = field(
        default=None,
        metadata={
            "name": "return",
        },
    )
