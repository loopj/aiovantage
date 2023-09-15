"""Base class for command client interfaces."""

from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast, overload

from aiovantage.command_client import CommandClient
from aiovantage.command_client.utils import (
    ParameterType,
    encode_params,
    parse_param,
    tokenize_response,
)

T = TypeVar("T")


class Interface:
    """Base class for command client object interfaces."""

    method_signatures: Dict[str, Type[Any]] = {}

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

    @overload
    async def invoke(self, vid: int, method: str, *params: ParameterType) -> Any:
        ...

    @overload
    async def invoke(
        self, vid: int, method: str, *params: ParameterType, as_type: Type[T]
    ) -> T:
        ...

    async def invoke(
        self,
        vid: int,
        method: str,
        *params: ParameterType,
        as_type: Optional[Type[T]] = None,
    ) -> Union[T, Any, None]:
        """Invoke a method on an object, and wait for a response.

        Args:
            vid: The VID of the object to invoke the command on.
            method: The method to invoke.
            params: The parameters to send with the method.
            as_type: The type to parse the response as.

        Returns:
            A parsed response, or None if no response was expected.
        """
        request = f"INVOKE {vid} {method}"
        if params:
            request += f" {encode_params(*params)}"

        # Send the request
        raw_response = await self.command_client.raw_request(request)

        # Ignore the response if we didn't specify a type to parse it as
        if not as_type:
            return None

        # Parse the response
        _, _, result, _, *args = tokenize_response(raw_response[0])
        return self.parse_response(result, method, *args, as_type=as_type)

    @overload
    @classmethod
    def parse_response(
        cls, result: str, method: str, *args: str, as_type: Type[T]
    ) -> T:
        ...

    @overload
    @classmethod
    def parse_response(cls, result: str, method: str, *args: str) -> Any:
        ...

    @classmethod
    def parse_response(
        cls, result: str, method: str, *args: str, as_type: Optional[Type[T]] = None
    ) -> Union[T, Any, None]:
        """Parse a response from an object interface."""
        # Get the signature of the method we are parsing the response for
        signature = cls._get_signature(method)

        # Return early if this method has no return value
        if signature is None:
            return None

        # Parse the response
        parsed_response: Any
        if issubclass(signature, tuple) and hasattr(signature, "__annotations__"):
            # If the signature is a NamedTuple, parse each component
            types = signature.__annotations__
            parsed_values: List[Any] = []
            for arg, klass in zip([result, *args], types.values()):
                parsed_values.append(parse_param(arg, klass))

            parsed_response = signature(*parsed_values)
        else:
            # Otherwise, we are dealing with a single return value, send it to parse_arg
            parsed_response = parse_param(result, signature)

        # Cast the result to as_type, if specified
        if as_type:
            return cast(T, parsed_response)

        # Return the parsed result
        return parsed_response

    @classmethod
    def _get_signature(cls, method: str) -> Optional[Type[Any]]:
        """Get the signature of a method."""
        # Instances can inherit from multiple interfaces, so let's find the response
        # parser for the method we just invoked.
        for klass in cls.__mro__:
            if issubclass(klass, Interface) and method in klass.method_signatures:
                return klass.method_signatures[method]

        return None
