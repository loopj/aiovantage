"""IIntrospection interface."""

from dataclasses import dataclass, field


@dataclass
class GetInterfaces:
    """IIntrospection.GetInterfaces method definition."""

    interface = "IIntrospection"

    @dataclass
    class Interface:
        """Object interface definition."""

        name: str
        version: str
        iid: int = field(metadata={"name": "IID"})

    call = None

    result: list[Interface] | None = field(
        default_factory=list,
        metadata={
            "wrapper": "return",
            "name": "Interface",
            "type": "Element",
        },
    )


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


@dataclass
class GetTypes:
    """IIntrospection.GetTypes method definition."""

    interface = "IIntrospection"

    @dataclass
    class Type:
        """Object type definition."""

        name: str
        version: str

    call = None

    result: list[Type] | None = field(
        default=None,
        metadata={
            "wrapper": "return",
            "name": "Type",
            "type": "Element",
        },
    )


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
