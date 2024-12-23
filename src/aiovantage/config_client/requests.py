"""Helper functions for fetching system objects."""

from collections.abc import AsyncIterator, Sequence
from contextlib import suppress
from typing import Any

from aiovantage.errors import ClientError, ClientResponseError

from . import ConfigClient
from .interfaces.configuration import (
    CloseFilter,
    GetFilterResults,
    GetObject,
    OpenFilter,
)
from .interfaces.introspection import GetVersion


async def get_objects(
    client: ConfigClient,
    *,
    types: Sequence[str] | None = None,
    xpath: str | None = None,
) -> AsyncIterator[Any]:
    """Get all vantage system objects of the specified types.

    Args:
        client: The config client instance
        types: An optional string, or list of strings of object types to fetch
        xpath: An optional xpath to filter the results by, eg. "/Load", "/*[@VID='12']"

    Yields:
        The objects of the specified types
    """
    # Support both a single object type and a list of status types
    if isinstance(types, str):
        types = [types]
    elif types is not None:
        types = list(types)

    # Open the filter
    handle = await client.request(
        OpenFilter, OpenFilter.Params(object_types=types, xpath=xpath)
    )

    if handle is None:
        raise ClientResponseError("Failed to open filter")

    try:
        # Get the results
        while True:
            response = await client.request(
                GetFilterResults, GetFilterResults.Params(h_filter=handle)
            )

            if not response:
                break

            for obj in response:
                yield obj.choice
    finally:
        # Close the filter
        with suppress(ClientError):
            await client.request(CloseFilter, handle)


async def get_objects_by_id(
    client: ConfigClient, vids: Sequence[int]
) -> AsyncIterator[Any]:
    """Get all vantage system objects of the specified ids.

    Args:
        client: The config client instance
        vids: A list of Vantage IDs for object to fetch

    Yields:
        The objects of the specified ids
    """
    # Open the filter
    response = await client.request(GetObject, GetObject.Params(vids=list(vids)))
    if not response:
        return

    for obj in response:
        yield obj.choice


async def get_object_by_id(client: ConfigClient, vid: int) -> Any:
    """Get a single Vantage system object by id.

    Args:
        client: The config client instance
        vid: The Vantage ID of the object to fetch

    Returns:
        The object matching the specified id, or None if not found
    """
    try:
        return await get_objects_by_id(client, [vid]).__anext__()
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
