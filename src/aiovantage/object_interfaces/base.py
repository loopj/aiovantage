"""Base class for command client interfaces."""

from typing import Any, TypeVar, get_type_hints, overload

from aiovantage.command_client import CommandClient
from aiovantage.command_client.types import converter

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
    async def invoke(self, vid: int, method: str, *params: Any) -> Any: ...

    @overload
    async def invoke(
        self, vid: int, method: str, *params: Any, as_type: type[T]
    ) -> T: ...

    async def invoke(
        self, vid: int, method: str, *params: Any, as_type: type[T] | None = None
    ) -> T | Any:
        """Invoke a method on an object, and return the parsed response.

        Args:
            vid: The VID of the object to invoke the command on.
            method: The method to invoke.
            params: The parameters to send with the method.
            as_type: The type to cast the response to.

        Returns:
            A parsed response, or None if no response was expected.
        """
        # Send the command
        response = await self.command_client.command(
            "INVOKE", vid, method, *params, force_quotes=True
        )

        # Break the response into tokens
        _id, result, _method, *args = response.args

        # Parse the response
        signature = as_type or self.get_method_signature(method)
        return _parse_object_response(result, *args, as_type=signature)

    @classmethod
    def get_method_signature(cls, method: str) -> type[Any] | None:
        """Get the signature of a method."""
        for klass in cls.__mro__:
            if issubclass(klass, Interface) and method in klass.method_signatures:
                return klass.method_signatures[method]

    @classmethod
    def parse_object_status(cls, method: str, result: str, *args: str) -> Any:
        """Handle an object interface status message.

        Args:
            method: The method that was invoked.
            result: The result of the command.
            args: The arguments that were sent with the command.
        """
        # Parse the response
        signature = cls.get_method_signature(method)
        return _parse_object_response(result, *args, as_type=signature)


def _parse_object_response(
    result: str, *args: str, as_type: type[T] | None
) -> T | None:
    """Parse an object interface response message.

    Args:
        result: The "result" of the command, aka the return value.
        args: The arguments that were sent with the command, which may have been modified.
        as_type: The expected return type of the method.

    Returns:
        A response parsed into the expected type.
    """
    # -> R:INVOKE <id> <result> <Interface.Method> <arg1> <arg2> ...
    # -> EL: <id> <Interface.Method> <result> <arg1> <arg2> ...
    # -> S:STATUS <id> <Interface.Method> <result> <arg1> <arg2> ...

    # Return early if the expected type is NoneType
    if as_type in (None, type(None)):
        return None

    # Otherwise, parse the result into the expected type
    if type_hints := get_type_hints(as_type):
        # Some methods return multiple values, in the "return" field and in the
        # "params" fields. This adds support for parsing multiple values into
        # a dataclass or NamedTuple.
        parsed_values: list[Any] = []
        for arg, klass in zip([result, *args], type_hints.values(), strict=True):
            parsed_value = converter.deserialize(klass, arg)
            parsed_values.append(parsed_value)

        parsed_response = as_type(*parsed_values)
    else:
        # Simple string responses contain the string value in the first argument
        param = args[0] if as_type is str else result
        parsed_response = converter.deserialize(as_type, param)

    # Return the parsed result
    return parsed_response
