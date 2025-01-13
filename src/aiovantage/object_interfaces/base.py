"""Base class for command client interfaces."""

# pyright: reportFunctionMemberAccess=false

from collections.abc import Callable
from typing import Any, ClassVar, Protocol, TypeVar, get_type_hints, runtime_checkable

from aiovantage.command_client import CommandClient
from aiovantage.command_client.utils import ParameterType, parse_object_response
from aiovantage.errors import NotImplementedError, NotSupportedError

T = TypeVar("T", bound=Callable[..., Any])


def method(method: str, *, property: str | None = None) -> Callable[[T], T]:
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

    def decorator(func: T) -> T:
        # Attach metadata to the function
        metadata: list[tuple[str, str | None]] = getattr(func, "method_metadata", [])
        metadata.append((method, property))
        func.method_metadata = metadata

        return func

    return decorator


@runtime_checkable
class MethodCallable(Protocol):
    """Protocol for an interface methods, with method metadata."""

    method_metadata: list[tuple[str, str | None]]

    async def __call__(self, *args: Any, **kwargs: Any) -> ParameterType: ...  # noqa: D102


class InterfaceMeta(type):
    """Metaclass to collect method metadata from member functions and base classes."""

    def __new__(
        cls: type["InterfaceMeta"],
        name: str,
        bases: tuple[type, ...],
        dct: dict[str, Any],
    ):
        """Create a new object interface class."""
        method_signatures: dict[str, type[ParameterType]] = {}
        method_properties: dict[str, str] = {}
        property_getters: dict[str, MethodCallable] = {}

        # Include method metadata from base classes
        for base in bases:
            if issubclass(base, Interface):
                method_signatures.update(base.method_signatures)
                method_properties.update(base.method_properties)
                property_getters.update(base.property_getters)

        # Collect method metadata from member functions
        for attr in dct.values():
            if not isinstance(attr, MethodCallable):
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

    method_signatures: ClassVar[dict[str, type[ParameterType]]]
    """A mapping of method names to return types, for parsing statuses and responses."""

    method_properties: ClassVar[dict[str, str]]
    """A mapping of method names to property names, for updating object state."""

    property_getters: ClassVar[dict[str, MethodCallable]]
    """A mapping of property names to getter functions, for fetching object state."""

    command_client: CommandClient | None = None
    """The command client to use for sending requests."""

    def __init__(self, command_client: CommandClient | None = None) -> None:
        """Initialize the interface with a command client."""
        self.command_client = command_client

    async def invoke(
        self, method: str, *params: ParameterType, as_type: type | None = None
    ) -> Any:
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

        # Get the expected return type of the method
        signature = as_type or self.method_signatures[method]

        # Invoke the method
        return await self.command_client.invoke(vid, method, *params, as_type=signature)

    async def fetch_state(self) -> list[str]:
        """Fetch state properties provided by the interface(s) this object implements.

        Args:
            fields: An optional list of fields to fetch, or None to fetch all.
        """
        cls = type(self)

        # Fetch each state property
        attrs_changed: list[str] = []
        for field in cls.property_getters.keys():
            if getter := cls.property_getters.get(field):
                # Call the getter function
                try:
                    result = await getter(self)
                except (NotImplementedError, NotSupportedError):
                    continue

                # Update the attribute if the result has changed
                if getattr(self, field) != result:
                    setattr(self, field, result)
                    attrs_changed.append(field)

        return attrs_changed

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
            return

        # Get the expected return type of the method
        signature = self.method_signatures.get(method)
        if signature is None:
            raise NotImplementedError(f"No signature found for method {method}")

        # Parse the response
        value = parse_object_response(result, *args, as_type=signature)

        # Update the property if it has changed
        if hasattr(self, property) and getattr(self, property) != value:
            setattr(self, property, value)
            return property
