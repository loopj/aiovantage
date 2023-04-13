from typing import AsyncIterator, List, Type, TypeVar

from aiovantage.aci_client import ACIClient
from aiovantage.aci_client.interfaces import IConfiguration
from aiovantage.aci_client.methods.configuration import (
    CloseFilter,
    GetFilterResults,
    ObjectFilter,
    OpenFilter,
)

T = TypeVar("T")


async def get_objects_by_type(
    client: ACIClient, vantage_types: List[str], base_type: Type[T]
) -> AsyncIterator[T]:
    """
    Helper function to get all objects of the specified types

    Args:
        client: The ACI client instance
        vantage_types: A list of Vantage object types to fetch
        base_type: The base type to cast the objects to

    Yields:
        The objects of the specified types
    """

    # Open the filter
    handle = await client.request(
        IConfiguration,
        OpenFilter,
        OpenFilter.Params(objects=ObjectFilter(object_type=vantage_types)),
    )

    # Get the results
    while True:
        response = await client.request(
            IConfiguration,
            GetFilterResults,
            GetFilterResults.Params(h_filter=handle),
        )

        if not response.object_value:
            break

        for object in response.object_value:
            if object.choice and isinstance(object.choice, base_type):
                yield object.choice
            else:
                print(f"Couldnt parse object with vid {object.id}")

    # Close the filter
    await client.request(IConfiguration, CloseFilter, handle)
