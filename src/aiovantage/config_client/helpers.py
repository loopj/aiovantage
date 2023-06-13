from typing import Any, AsyncIterator, Sequence

from aiovantage.config_client import ConfigClient
from aiovantage.config_client.methods.configuration import (
    CloseFilter,
    GetFilterResults,
    GetObject,
    OpenFilter,
)


async def get_objects_by_type(
    client: ConfigClient, types: Sequence[str]
) -> AsyncIterator[Any]:
    """
    Helper function to get all vantage system objects of the specified types

    Args:
        client: The ACI client instance
        types: A list of strings of the Vantage object types to fetch

    Yields:
        The objects of the specified types
    """

    try:
        # Open the filter
        handle = await client.request(
            OpenFilter,
            OpenFilter.Params(objects=OpenFilter.Filter(object_type=list(types))),
        )

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
