"""Base class for command client interfaces."""

import inspect
from collections.abc import Callable, Sequence
from enum import Enum
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

from typing_extensions import Self

from aiovantage.command_client import CommandClient
from aiovantage.command_client.types import converter
from aiovantage.errors import NotImplementedError, NotSupportedError

T = TypeVar("T")


class _AsyncCallable(Protocol):
    async def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


@runtime_checkable
class _MethodCallable(Protocol):
    method_metadata: list[tuple[str, str | None]]

    async def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


def method(
    method: str, *, property: str | None = None
) -> Callable[[_AsyncCallable], _AsyncCallable]:
    """Decorator to annotate a function as a Vantage method.

    This is used to automatically keep track of expected return types for
    Vantage method calls so we can parse responses correctly, both when
    directly invoking methods and when receiving status messages.

    Optionally, a property name can be associated with the method, which can
    be used to update the state of the object when receiving status messages,
    or to fetch the initial state of the object.

    Args:
        method: The vantage method name to associate with the function.
        property: Optional property name to associate with the function.
    """

    def decorator(func: _AsyncCallable) -> _AsyncCallable:
        # Attach metadata to the function
        metadata: list[tuple[str, str | None]] = getattr(func, "method_metadata", [])
        metadata.append((method, property))

        func = cast(_MethodCallable, func)
        func.method_metadata = metadata

        return func

    return decorator


def interface_enums() -> dict[str, type[Enum]]:
    """Return all enums provided by object interfaces."""
    enum_classes: dict[str, type[Enum]] = {}

    for cls in Interface.__subclasses__():
        # Iterate over all members of the class
        for _name, obj in inspect.getmembers(cls):
            if inspect.isclass(obj) and issubclass(obj, Enum):
                enum_classes[f"{cls.interface_name}_{obj.__name__}"] = obj

    return enum_classes


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
                type_hints = get_type_hints(attr)
                if "return" not in type_hints:
                    raise NotImplementedError(f"Return type missing for {method}")

                method_signatures[method] = type_hints["return"]
                if property:
                    method_properties[method] = property
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

    def __init__(self, command_client: CommandClient | None = None) -> None:
        """Initialize the interface with a command client."""
        self.command_client = command_client

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
        # Make sure we have a vid to invoke the method on
        if (vid := getattr(self, "vid", None)) is None:
            raise ValueError("The object must have a vid attribute to invoke methods.")

        # Make sure we have a command client to send requests with
        if self.command_client is None:
            raise ValueError("The object has no command client to send requests with.")

        # Make sure we have a signature for the method
        if as_type is None and method not in self.method_signatures:
            raise NotImplementedError(f"No signature found for method {method}")

        # Send the command
        response = await self.command_client.command(
            "INVOKE", vid, method, *params, force_quotes=True
        )

        # Break the response into tokens
        _id, result, _method, *args = response.args

        # Parse the response
        signature = as_type or self.method_signatures[method]
        return _parse_object_response(result, *args, as_type=signature)

    async def fetch_state(self, properties: Sequence[str] | None = None) -> list[str]:
        """Fetch state properties provided by the interface(s) this object implements."""
        cls = type(self)

        # Determine which properties to fetch
        props_to_fetch = (
            [prop for prop in properties if prop in cls.property_getters.keys()]
            if properties is not None
            else cls.property_getters.keys()
        )

        # Fetch each state property
        props_changed: list[str] = []
        for prop in props_to_fetch:
            if getter := cls.property_getters.get(prop):
                # Call the getter function
                try:
                    result = await getter(self)
                except (NotImplementedError, NotSupportedError):
                    continue

                # Update the attribute if the result has changed
                if getattr(self, prop) != result:
                    setattr(self, prop, result)
                    props_changed.append(prop)

        return props_changed

    def handle_object_status(self, method: str, result: str, *args: str) -> str | None:
        """Handle an object interface status message.

        Args:
            method: The method that was invoked.
            result: The result of the command.
            args: The arguments that were sent with the command.
        """
        # Look up the property associated with this method
        property = self.method_properties.get(method)
        if property is None:
            return None

        # Make sure we have a signature for the method
        if method not in self.method_signatures:
            raise NotImplementedError(f"No signature found for method {method}")

        # Parse the response
        signature = self.method_signatures[method]
        value = _parse_object_response(result, *args, as_type=signature)

        # Update the property if it has changed
        if hasattr(self, property) and getattr(self, property) != value:
            setattr(self, property, value)
            return property

    @classmethod
    def implementers(cls) -> set[type[Self]]:
        """Return the subclasses of this object."""
        return set(cls.__subclasses__()).union(
            subclass for sub in cls.__subclasses__() for subclass in sub.implementers()
        )


def _parse_object_response(result: str, *args: str, as_type: type[T]) -> T | None:
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
    if as_type is type(None):
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
