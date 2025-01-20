"""Helper functions for fetching system objects."""

from collections.abc import AsyncIterator
from contextlib import suppress
from typing import TypeVar

from aiovantage.errors import ClientError, ClientResponseError
from aiovantage.objects import SystemObject

from . import ConfigClient
from .interfaces.configuration import (
    CloseFilter,
    GetFilterResults,
    GetObject,
    OpenFilter,
)
from .interfaces.introspection import GetVersion

T = TypeVar("T", bound=SystemObject)


async def get_objects(
    client: ConfigClient, *types: str, xpath: str | None = None
) -> AsyncIterator[SystemObject]:
    """Get all vantage system objects of the specified types.

    Args:
        client: The config client instance
        *types: The element names of the objects to fetch
        xpath: An optional xpath to filter the results by, eg. "/Load", "/*[@VID='12']"

    Yields:
        The objects of the specified types
    """
    # Open the filter
    handle = await client.request(
        OpenFilter, OpenFilter.Params(object_types=list(types), xpath=xpath)
    )

    if handle is None:
        raise ClientResponseError("Failed to open filter")

    try:
        while response := await client.request(
            GetFilterResults, GetFilterResults.Params(h_filter=handle)
        ):
            for obj in response:
                if not isinstance(obj.choice, SystemObject):
                    continue

                yield obj.choice
    finally:
        # Close the filter
        with suppress(ClientError):
            await client.request(CloseFilter, handle)


async def get_objects_by_type(
    client: ConfigClient, object_type: type[T], xpath: str | None = None
) -> AsyncIterator[T]:
    """Get all vantage system objects of the specified type.

    Args:
        client: The config client instance
        object_type: The type of objects to fetch
        xpath: An optional xpath to filter the results by, eg. "/Load", "/*[@VID='12']"

    Yields:
        The objects of the specified types
    """
    async for obj in get_objects(client, object_type.element_name(), xpath=xpath):
        if isinstance(obj, object_type):
            yield obj


async def get_objects_by_id(
    client: ConfigClient, *vids: int
) -> AsyncIterator[SystemObject]:
    """Get all vantage system objects of the specified ids.

    Args:
        client: The config client instance
        *vids: A list of Vantage IDs of objects to fetch

    Yields:
        The objects of the specified ids
    """
    # Open the filter
    response = await client.request(GetObject, GetObject.Params(vids=list(vids)))
    if not response:
        return

    for obj in response:
        if not isinstance(obj.choice, SystemObject):
            raise ClientResponseError(f"Unsupported object type: {type(obj.choice)}")

        yield obj.choice


async def get_object_by_id(client: ConfigClient, vid: int) -> SystemObject | None:
    """Get a single Vantage system object by id.

    Args:
        client: The config client instance
        vid: The Vantage ID of the object to fetch

    Returns:
        The object matching the specified id, or None if not found
    """
    try:
        return await get_objects_by_id(client, vid).__anext__()
    except StopAsyncIteration:
        return None


async def get_version(client: ConfigClient) -> str | None:
    """Get the firmware version of the Vantage controller.

    Args:
        client: The config client instance.
    """
    version = await client.request(GetVersion)
    if version is None:
        return None

    return version.app
