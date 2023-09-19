"""Base class for command client interfaces."""

from typing import Any, TypeVar, overload

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

    method_signatures: dict[str, type[Any]] = {}

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
        self, vid: int, method: str, *params: ParameterType, as_type: type[T]
    ) -> T:
        ...

    async def invoke(
        self,
        vid: int,
        method: str,
        *params: ParameterType,
        as_type: type[T] | None = None,
    ) -> T | Any | None:
        """Invoke a method on an object, and return the parsed response.

        Args:
            vid: The VID of the object to invoke the command on.
            method: The method to invoke.
            params: The parameters to send with the method.
            as_type: The type to cast the response to.

        Returns:
            A parsed response, or None if no response was expected.
        """
        # INVOKE <id> <Interface.Method>
        # -> R:INVOKE <id> <result> <Interface.Method> <arg1> <arg2> ...
        request = f"INVOKE {vid} {method}"
        if params:
            request += f" {encode_params(*params)}"

        # Send the request
        raw_response = await self.command_client.raw_request(request)

        # Break the response into tokens
        _, _, result, _, *args = tokenize_response(raw_response[0])

        # Parse the response
        if as_type is None:
            return self.parse_response(method, result, *args)
        return self.parse_response(method, result, *args, as_type=as_type)

    @overload
    @classmethod
    def parse_response(
        cls, method: str, result: str, *args: str, as_type: type[T]
    ) -> T:
        ...

    @overload
    @classmethod
    def parse_response(cls, method: str, result: str, *args: str) -> Any:
        ...

    @classmethod
    def parse_response(
        cls, method: str, result: str, *args: str, as_type: type[T] | None = None
    ) -> T | Any | None:
        """Parse an object interface "INVOKE" response or status message.

        Args:
            method: The method that was invoked.
            result: The result of the command.
            args: The arguments that were sent with the command.
            as_type: The type to cast the response to.

        Returns:
            A parsed response, or None if no response was expected.
        """
        # -> R:INVOKE <id> <result> <Interface.Method> <arg1> <arg2> ...
        # -> EL: <id> <Interface.Method> <result> <arg1> <arg2> ...
        # -> S:STATUS <id> <Interface.Method> <result> <arg1> <arg2> ...

        # Get the signature of the method we are parsing the response for
        signature = as_type or cls._get_signature(method)

        # Return early if this method has no return value
        if signature is None:
            return None

        # Parse the response
        parsed_response: Any
        if issubclass(signature, tuple) and hasattr(signature, "__annotations__"):
            # If the signature is a NamedTuple, parse each component
            parsed_values: list[Any] = []
            for arg, klass in zip(
                [result, *args], signature.__annotations__.values(), strict=True
            ):
                parsed_values.append(parse_param(arg, klass))

            parsed_response = signature(*parsed_values)
        else:
            # Otherwise, parse a single return value
            parsed_response = parse_param(result, signature)

        # Return the parsed result
        return parsed_response

    @classmethod
    def _get_signature(cls, method: str) -> type[Any] | None:
        # Get the signature of a method.
        for klass in cls.__mro__:
            if issubclass(klass, Interface) and method in klass.method_signatures:
                return klass.method_signatures[method]

        return None
