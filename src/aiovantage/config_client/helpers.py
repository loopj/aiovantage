from typing import Any, AsyncIterator, List, Optional, Type, TypeVar, Union, overload

from aiovantage.config_client import ConfigClient
from aiovantage.config_client.methods.configuration import (
    CloseFilter,
    GetFilterResults,
    OpenFilter,
    GetObject,
)

T = TypeVar("T")


@overload
def get_objects_by_type(
    client: ConfigClient, types: List[str], base: Type[T]
) -> AsyncIterator[T]:
    """
    Helper function to get all vantage system objects of the specified types

    Args:
        client: The ACI client instance
        types: A list of Vantage object types to fetch
        base: The base class to validate the objects against

    Yields:
        The objects of the specified types
    """
    ...


@overload
def get_objects_by_type(client: ConfigClient, types: List[str]) -> AsyncIterator[Any]:
    """
    Helper function to get all vantage system objects of the specified types

    Args:
        client: The ACI client instance
        types: A list of strings of the Vantage object types to fetch

    Yields:
        The objects of the specified types
    """
    ...


async def get_objects_by_type(
    client: ConfigClient, types: List[str], base: Optional[Type[T]] = None
) -> AsyncIterator[Union[T, Any]]:
    # Open the filter
    handle = await client.request(
        OpenFilter, OpenFilter.Params(objects=OpenFilter.Filter(object_type=types))
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

            if base is None:
                yield object.choice
            elif isinstance(object.choice, base):
                yield object.choice
            else:
                client._logger.warning(
                    f"Object {object.id} is not expected type. Expected "
                    f"{base.__name__} but got {type(object.choice).__name__}"
                )

    # Close the filter
    await client.request(CloseFilter, handle)


@overload
def get_objects_by_id(
    client: ConfigClient, ids: List[int], base: Type[T]
) -> AsyncIterator[T]:
    """
    Helper function to get all vantage system objects of the specified ids

    Args:
        client: The ACI client instance
        ids: A list of Vantage object ids to fetch
        base: The base class to validate the objects against

    Yields:
        The objects of the specified ids
    """
    ...


@overload
def get_objects_by_id(client: ConfigClient, ids: List[int]) -> AsyncIterator[Any]:
    """
    Helper function to get all vantage system objects of the specified ids

    Args:
        client: The ACI client instance
        ids: A list of integers of the Vantage object ids to fetch

    Yields:
        The objects of the specified ids
    """
    ...


async def get_objects_by_id(
    client: ConfigClient, ids: List[int], base: Optional[Type[T]] = None
) -> AsyncIterator[Union[T, Any]]:
    # Open the filter
    response = await client.request(GetObject, GetObject.Params(vids=ids))
    if not response.objects:
        return

    for object in response.objects:
        if object.choice is None:
            continue

        if base is None:
            yield object.choice
        elif isinstance(object.choice, base):
            yield object.choice
        else:
            client._logger.warning(
                f"Object {object.id} is not expected type. Expected "
                f"{base.__name__} but got {type(object.choice).__name__}"
            )


async def get_object_by_id(client: ConfigClient, id: int, base: Type[T]) -> Optional[T]:
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
        return await get_objects_by_id(client, [id], base).__anext__()
    except StopAsyncIteration:
        return None
