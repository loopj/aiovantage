from collections.abc import AsyncIterator
from contextlib import suppress
from dataclasses import dataclass, field
from typing import Any, TypeVar, overload

from aiovantage.errors import ClientError

from ..client import ConfigClient

T = TypeVar("T")


@dataclass
class WrappedObject:
    # Wildcard type that can be used to represent any object.
    vid: int = field(metadata={"name": "VID", "type": "Attribute"})
    obj: object = field(metadata={"type": "Wildcard"})


@dataclass
class OpenFilter:
    @dataclass
    class Params:
        object_types: list[str] | None = field(
            default=None,
            metadata={"wrapper": "Objects", "name": "ObjectType", "type": "Element"},
        )
        xpath: str | None = field(default=None, metadata={"name": "XPath"})

    call: Params | None = field(default=None, metadata={"name": "call"})
    result: int | None = field(default=None, metadata={"name": "return"})


@dataclass
class GetFilterResults:
    @dataclass
    class Params:
        h_filter: int = field(metadata={"name": "hFilter"})
        count: int = 50
        whole_object: bool = True

    call: Params | None = field(default=None, metadata={"name": "call"})
    result: list[WrappedObject] | None = field(
        default_factory=list,
        metadata={"wrapper": "return", "name": "Object", "type": "Element"},
    )


@dataclass
class CloseFilter:
    call: int | None = field(default=None, metadata={"name": "call"})
    result: bool | None = field(default=None, metadata={"name": "return"})


@dataclass
class GetObject:
    call: list[int] | None = field(
        default_factory=list,
        metadata={"wrapper": "call", "name": "VID", "type": "Element"},
    )

    result: list[WrappedObject] | None = field(
        default_factory=list,
        metadata={"wrapper": "return", "name": "Object", "type": "Element"},
    )


@dataclass(kw_only=True)
class IConfiguration:
    open_filter: OpenFilter | None = None
    get_filter_results: GetFilterResults | None = None
    close_filter: CloseFilter | None = None
    get_object: GetObject | None = None


class ConfigurationInterface:
    """Wrapper for the `IConfiguration` RPC interface."""

    @staticmethod
    async def open_filter(
        client: ConfigClient, *object_types: str, xpath: str | None = None
    ) -> int:
        """Open a filter for fetching Vantage objects.

        Args:
            client: A config client instance
            *object_types: The type names of the objects to fetch, eg. "Area", "Load", "Keypad"
            xpath: An optional xpath to filter the results by, eg. "/Load", "/*[@VID='12']"

        Returns:
            The handle of the opened filter
        """
        return await client.rpc(
            IConfiguration,
            OpenFilter,
            OpenFilter.Params(object_types=list(object_types), xpath=xpath),
        )

    @staticmethod
    async def get_filter_results(
        client: ConfigClient, h_filter: int, count: int = 50, whole_object: bool = True
    ) -> list[WrappedObject]:
        """Get results from a filter handle previously opened with open_filter.

        Args:
            client: A config client instance
            h_filter: The handle of the filter to fetch results for
            count: The maximum number of results to fetch
            whole_object: Whether to fetch the whole object or a compact representation

        Returns:
            A list of Vantage objects
        """
        return await client.rpc(
            IConfiguration, GetFilterResults, GetFilterResults.Params(h_filter)
        )

    @staticmethod
    async def close_filter(client: ConfigClient, h_filter: int) -> bool:
        """Close a filter handle previously opened with open_filter.

        Args:
            client: A config client instance
            h_filter: The handle of the filter to close

        Returns:
            True if the filter was closed successfully, False otherwise
        """
        return await client.rpc(IConfiguration, CloseFilter, h_filter)

    @staticmethod
    async def get_object(client: ConfigClient, *vids: int) -> list[WrappedObject]:
        """Get one or more Vantage objects by their VIDs.

        Args:
            client: A config client instance
            *vids: The VIDs of the objects to fetch

        Returns:
            A list of Vantage objects
        """
        return await client.rpc(IConfiguration, GetObject, list(vids))

    # Convenience functions, not part of the interface
    @overload
    @staticmethod
    def get_objects(
        client: ConfigClient, *types: str, xpath: str | None = None, as_type: type[T]
    ) -> AsyncIterator[T]: ...

    @overload
    @staticmethod
    def get_objects(
        client: ConfigClient, *types: str, xpath: str | None = None
    ) -> AsyncIterator[Any]: ...

    @staticmethod
    async def get_objects(
        client: ConfigClient,
        *types: str,
        xpath: str | None = None,
        as_type: type[T] | None = None,
    ) -> AsyncIterator[T | Any]:
        """Get Vantage objects, optionally filtered by a type and/or an XPath.

        This is a convenience function that wraps the open_filter, get_filter_results
        and close_filter methods.

        Args:
            client: A config client instance
            *types: The type names of the objects to fetch, eg. "Area", "Load", "Keypad"
            xpath: An optional xpath to filter the results by, eg. "/Load", "/*[@VID='12']"
            as_type: The type to verify the objects as

        Yields:
            A stream of Vantage objects
        """
        # Open the filter
        handle = await ConfigurationInterface.open_filter(client, *types, xpath=xpath)

        try:
            # Fetch the results
            while objects := await ConfigurationInterface.get_filter_results(
                client, handle
            ):
                for obj in objects:
                    if as_type is None or isinstance(obj.obj, as_type):
                        yield obj.obj
        finally:
            # Close the filter
            with suppress(ClientError):
                await ConfigurationInterface.close_filter(client, handle)
