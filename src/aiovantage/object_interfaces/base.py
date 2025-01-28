"""Base class for command client interfaces."""

from collections.abc import Callable
from typing import (
    Any,
    ClassVar,
    Protocol,
    TypeVar,
    cast,
    get_type_hints,
    overload,
    runtime_checkable,
)

from aiovantage.command_client import CommandClient
from aiovantage.command_client.types import converter

T = TypeVar("T")


class _AsyncCallable(Protocol):
    async def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


@runtime_checkable
class _MethodCallable(Protocol):
    method_metadata: list[tuple[str, str | None]]

    async def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


def method(
    *methods: str, property: str | None = None
) -> Callable[[_AsyncCallable], _AsyncCallable]:
    """Decorator to annotate a function as a Vantage method.

    This is used to automatically keep track of expected return types for
    Vantage method calls so we can parse responses correctly, both when
    directly invoking methods and when receiving status messages.

    Optionally, a property name can be associated with the method, which can
    be used to update the state of the object when receiving status messages,
    or to fetch the initial state of the object.

    Args:
        methods: The vantage method names to associate with the function.
        property: Optional property name to associate with the function.
    """

    def decorator(func: _AsyncCallable) -> _AsyncCallable:
        # Attach metadata to the function
        metadata: list[tuple[str, str | None]] = getattr(func, "method_metadata", [])

        for method in methods:
            metadata.append((method, property))

        func = cast(_MethodCallable, func)
        func.method_metadata = metadata

        return func

    return decorator


class InterfaceMeta(type):
    """Metaclass to collect method metadata from member functions and base classes."""

    def __new__(
        cls: type["InterfaceMeta"],
        name: str,
        bases: tuple[type, ...],
        dct: dict[str, Any],
    ):
        """Create a new object interface class."""
        method_signatures: dict[str, type[Any]] = {}
        method_properties: dict[str, str] = {}
        property_getters: dict[str, _AsyncCallable] = {}

        # Include method metadata from base classes
        for base in bases:
            if issubclass(base, Interface):
                method_signatures.update(base.method_signatures)
                method_properties.update(base.method_properties)
                property_getters.update(base.property_getters)

        # Collect method metadata from member functions
        for attr in dct.values():
            if not isinstance(attr, _MethodCallable):
                continue

            for method, property in attr.method_metadata:
                # Get the return type of the method
                type_hints = get_type_hints(attr)
                if "return" not in type_hints:
                    raise NotImplementedError(f"Return type missing for {method}")

                # Get the fully-qualified method name
                fq_method = f"{dct['interface_name']}.{method}"

                # Attach the method signature to the class
                method_signatures[fq_method] = type_hints["return"]

                # Attach the property information to the class
                if property:
                    method_properties[fq_method] = property
                    property_getters[property] = attr

        # Attach the method metadata to the class
        dct["method_signatures"] = method_signatures
        dct["method_properties"] = method_properties
        dct["property_getters"] = property_getters

        return super().__new__(cls, name, bases, dct)


class Interface(metaclass=InterfaceMeta):
    """Base class for command client object interfaces."""

    interface_name: ClassVar[str]
    """The name of the interface."""

    method_signatures: ClassVar[dict[str, type[Any]]]
    """A mapping of method names to return types, for parsing statuses and responses."""

    method_properties: ClassVar[dict[str, str]]
    """A mapping of method names to property names, for updating object state."""

    property_getters: ClassVar[dict[str, _AsyncCallable]]
    """A mapping of property names to getter functions, for fetching object state."""

    command_client: CommandClient | None = None
    """The command client to use for sending requests."""

    vid: int
    """The VID of the object to send requests to."""

    @overload
    async def invoke(self, method: str, *params: Any) -> Any: ...

    @overload
    async def invoke(self, method: str, *params: Any, as_type: type[T]) -> T: ...

    async def invoke(
        self, method: str, *params: Any, as_type: type[T] | None = None
    ) -> T | Any:
        """Invoke a method on an object, and return the parsed response.

        Args:
            method: The method to invoke.
            params: The parameters to send with the method.
            as_type: The expected return type of the method, will attempt to infer if not provided.

        Returns:
            A parsed response, or None if no response was expected.
        """
        # Make sure we have a command client to send requests with
        if self.command_client is None:
            raise ValueError("The object has no command client to send requests with.")

        # Make sure we have a signature for the method
        if as_type is None and method not in self.method_signatures:
            raise NotImplementedError(f"No signature found for method {method}")

        # Send the command
        response = await self.command_client.command(
            "INVOKE", self.vid, method, *params, force_quotes=True
        )

        # Break the response into tokens
        _id, result, _method, *args = response.args

        # Parse the response
        signature = as_type or self.method_signatures[method]
        return _parse_object_response(result, *args, as_type=signature)

    @classmethod
    def parse_object_status(cls, method: str, result: str, *args: str) -> Any:
        """Handle an object interface status message.

        Args:
            method: The method that was invoked.
            result: The result of the command.
            args: The arguments that were sent with the command.
        """
        # Parse the response
        signature = cls.method_signatures[method]
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
