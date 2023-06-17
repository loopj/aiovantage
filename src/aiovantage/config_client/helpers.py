from typing import Any, AsyncIterator, Optional, Sequence

from aiovantage.config_client import ConfigClient
from aiovantage.config_client.methods.configuration import (
    CloseFilter,
    GetFilterResults,
    GetObject,
    OpenFilter,
)


async def get_objects(
    client: ConfigClient,
    *,
    type: Optional[Sequence[str]] = None,
    xpath: Optional[str] = None,
) -> AsyncIterator[Any]:
    """
    Helper function to get all vantage system objects of the specified types

    Args:
        client: The ACI client instance
        object_types: An optional string, or list of strings of object types to fetch
        xpath: An optional xpath to filter the results by, eg. "/Load", "/*[@VID='12']"

    Yields:
        The objects of the specified types
    """

    # Support both a single object type and a list of status types
    if isinstance(type, str):
        type_filter = OpenFilter.Filter(object_type=[type])
    elif type is None:
        type_filter = None
    else:
        type_filter = OpenFilter.Filter(object_type=list(type))

    # Open the filter
    handle = await client.request(
        OpenFilter, OpenFilter.Params(objects=type_filter, xpath=xpath)
    )

    try:
        # Get the results
        while True:
            response = await client.request(
                GetFilterResults, GetFilterResults.Params(h_filter=handle)
            )

            if not response.objects:
                break

            for object in response.objects:
                if object.choice is None:
                    continue

                yield object.choice
    finally:
        # Close the filter
        await client.request(CloseFilter, handle)


async def get_objects_by_id(
    client: ConfigClient, ids: Sequence[int]
) -> AsyncIterator[Any]:
    """
    Helper function to get all vantage system objects of the specified ids

    Args:
        client: The ACI client instance
        ids: A list of integers of the Vantage object ids to fetch

    Yields:
        The objects of the specified ids
    """

    # Open the filter
    response = await client.request(GetObject, GetObject.Params(vids=list(ids)))
    if not response.objects:
        return

    for object in response.objects:
        if object.choice is None:
            continue

        yield object.choice


async def get_object_by_id(client: ConfigClient, id: int) -> Any:
    """
    Helper function to get a single Vantage system object by id

    Args:
        client: The ACI client instance
        id: The id of the Vantage object to fetch
        base: The base class to validate the object against

    Returns:
        The object matching the specified id, or None if not found
    """

    try:
        return await get_objects_by_id(client, [id]).__anext__()
    except StopAsyncIteration:
        return None
