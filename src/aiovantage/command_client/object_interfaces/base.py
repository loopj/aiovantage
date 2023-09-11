"""Base class for command client interfaces."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Callable, Dict, Optional, Sequence, Type, TypeVar, Union, cast

from aiovantage.command_client import CommandClient
from aiovantage.command_client.utils import encode_params, tokenize_response

T = TypeVar("T")


@dataclass
class InterfaceResponse:
    """Wrapper for object interface invoke/status responses."""

    vid: int
    result: str
    method: str
    args: Sequence[str]


class Interface:
    """Base class for command client object interfaces."""

    response_parsers: Dict[str, Callable[[InterfaceResponse], Any]] = {}

    def __init__(self, client: CommandClient) -> None:
        """Initialize an object interface for standalone use.

        Args:
            client: The command client to use.
        """
        self._command_client = client

    @property
    def command_client(self) -> CommandClient:
        """Return the command client."""
        return self._command_client

    async def invoke(
        self, vid: int, method: str, *params: Union[str, int, float, Decimal]
    ) -> InterfaceResponse:
        """Invoke a method on an object, and wait for a response.

        Args:
            vid: The VID of the object to invoke the command on.
            method: The method to invoke.
            params: The parameters to send with the method.

        Returns:
            An InterfaceResponse instance.
        """
        if params:
            request = f"INVOKE {vid} {method} {encode_params(*params)}"
        else:
            request = f"INVOKE {vid} {method}"

        # Send the request and parse the response
        raw_response = await self.command_client.raw_request(request)
        _, vid_str, result, _, *args = tokenize_response(raw_response[-1])
        return InterfaceResponse(int(vid_str), result, method, args)

    @classmethod
    def parse_response(
        cls, response: InterfaceResponse, clazz: Optional[Type[T]] = None
    ) -> T:
        """Parse a response from an object interface.

        Args:
            response: The response to parse.
            clazz: The type to parse the response as.

        Returns:
            The parsed response.
        """
        return cast(T, cls.response_parsers[response.method](response))
