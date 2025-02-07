"""IIntrospection interface."""

from dataclasses import dataclass, field

from aiovantage.config_client._client import ConfigClient


@dataclass
class GetInterfaces:
    """IIntrospection.GetInterfaces method definition."""

    @dataclass
    class Interface:
        """Object interface definition."""

        name: str
        version: str
        iid: int = field(metadata={"name": "IID"})

    call = None
    result: list[Interface] | None = field(
        default_factory=list,
        metadata={"wrapper": "return", "name": "Interface", "type": "Element"},
    )


@dataclass
class GetSysInfo:
    """IIntrospection.GetSysInfo method definition."""

    @dataclass
    class SysInfo:
        """SysInfo class."""

        master_number: int
        serial_number: int

    call = None
    result: SysInfo | None = field(
        default=None, metadata={"wrapper": "return", "name": "SysInfo"}
    )


@dataclass
class GetTypes:
    """IIntrospection.GetTypes method definition."""

    @dataclass
    class Type:
        """Object type definition."""

        name: str
        version: str

    call = None
    result: list[Type] | None = field(
        default=None, metadata={"wrapper": "return", "name": "Type", "type": "Element"}
    )


@dataclass
class GetVersion:
    """IIntrospection.GetVersion method definition."""

    @dataclass
    class Version:
        """Method return value."""

        kernel: str | None = field(default=None, metadata={"name": "kernel"})
        rootfs: str | None = field(default=None, metadata={"name": "rootfs"})
        app: str | None = field(default=None, metadata={"name": "app"})

    call = None
    result: Version | None = field(default=None, metadata={"name": "return"})


@dataclass(kw_only=True)
class IIntrospection:
    """IIntrospection interface."""

    get_interfaces: GetInterfaces | None = None
    get_sys_info: GetSysInfo | None = None
    get_types: GetTypes | None = None
    get_version: GetVersion | None = None


class IntrospectionInterface:
    """Introspection interface."""

    @staticmethod
    async def get_interfaces(client: ConfigClient) -> list[GetInterfaces.Interface]:
        """Get a list of all interfaces on the device.

        Args:
            client: A config client instance

        Returns:
            A list of interfaces.
        """
        return await client.rpc_call(IIntrospection, GetInterfaces)

    @staticmethod
    async def get_sys_info(client: ConfigClient) -> GetSysInfo.SysInfo:
        """Get system information.

        Args:
            client: A config client instance

        Returns:
            A system information object.
        """
        return await client.rpc_call(IIntrospection, GetSysInfo)

    @staticmethod
    async def get_types(client: ConfigClient) -> list[GetTypes.Type]:
        """Get a list of all object types on the device.

        Args:
            client: A config client instance

        Returns:
            A list of object types.
        """
        return await client.rpc_call(IIntrospection, GetTypes)

    @staticmethod
    async def get_version(client: ConfigClient) -> GetVersion.Version:
        """Get the version of the device.

        Args:
            client: A config client instance

        Returns:
            A version information object.
        """
        return await client.rpc_call(IIntrospection, GetVersion)
