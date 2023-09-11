"""Base class for command client interfaces."""

from dataclasses import dataclass
from decimal import Decimal
from enum import IntEnum
from typing import Sequence, Type, TypeVar, Union

from aiovantage.command_client import CommandClient
from aiovantage.command_client.utils import encode_params, tokenize_response


@dataclass
class InterfaceResponse:
    """Wrapper for object interface invoke/status responses."""

    vid: int
    result: str
    method: str
    args: Sequence[str]


class Interface:
    """Base class for command client object interfaces."""

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


T = TypeVar("T", bound=IntEnum)


def fixed_to_decimal(value: str) -> Decimal:
    """Convert a Vantage fixed-point value to a Decimal."""
    # Handles both 123000 and 123.000 style fixed-point values
    return Decimal(value.replace(".", "")) / 1000


def fixed_result(response: InterfaceResponse) -> Decimal:
    """Parse a fixed-point result."""
    return fixed_to_decimal(response.result)


def int_result(response: InterfaceResponse) -> int:
    """Parse an integer result."""
    return int(response.result)


def bool_result(response: InterfaceResponse) -> bool:
    """Parse a boolean result."""
    return bool(int(response.result))


def enum_result(enum_cls: Type[T], response: InterfaceResponse) -> T:
    """Parse an enum result."""
    if response.result.isdigit():
        return enum_cls(int(response.result))

    return enum_cls[response.result]
