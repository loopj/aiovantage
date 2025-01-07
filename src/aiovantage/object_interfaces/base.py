"""Base class for command client interfaces."""

from collections.abc import Callable, Sequence
from typing import Any, TypeVar, get_type_hints

from aiovantage.command_client import CommandClient
from aiovantage.command_client.utils import ParameterType, parse_object_response
from aiovantage.errors import NotImplementedError

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
        # Make sure the method has a return type defined
        return_type = get_type_hints(func).get("return")
        if return_type is None:
            raise ValueError(f"Method {method} has no return type defined")

        # Attach metadata to the function
        func._method = method  # type: ignore
        func._property = property  # type: ignore
        func._return_type = return_type  # type: ignore

        return func

    return decorator


class InterfaceMeta(type):
    """Metaclass to collect method metadata from member functions and base classes."""

    method_signatures: dict[str, type]
    property_getters: dict[str, Any]

    def __new__(
        cls: type["InterfaceMeta"],
        name: str,
        bases: tuple[type, ...],
        dct: dict[str, Any],
    ):
        """Create a new object interface class."""
        cls_obj = super().__new__(cls, name, bases, dct)
        cls_obj.method_signatures = {}
        cls_obj.property_getters = {}

        # Include method metadata from base classes
        for base in bases:
            if issubclass(base, Interface):
                cls_obj.method_signatures.update(base.method_signatures)
                cls_obj.property_getters.update(base.property_getters)

        # Collect method metadata from member functions
        for attr in dct.values():
            if hasattr(attr, "_method") and hasattr(attr, "_return_type"):
                cls_obj.method_signatures[attr._method] = attr._return_type

            if hasattr(attr, "_property") and attr._property:
                cls_obj.property_getters[attr._property] = attr

        return cls_obj


class Interface(metaclass=InterfaceMeta):
    """Base class for command client object interfaces."""

    command_client: CommandClient | None = None
    """The command client to use for sending requests."""

    def __init__(self, command_client: CommandClient | None = None) -> None:
        """Initialize the interface with a command client."""
        self.command_client = command_client

    @classmethod
    def parse_status(cls, method: str, result: str, *args: str) -> Any:
        """Parse an object interface status message.

        Args:
            method: The method that was invoked.
            result: The result of the command.
            args: The arguments that were sent with the command.

        Returns:
            A parsed response, or None if no response was expected.
        """
        # Get the expected return type of the method
        signature = cls.method_signatures[method]

        # Parse the response
        return parse_object_response(result, *args, as_type=signature)  # type: ignore

    async def invoke(self, method: str, *params: ParameterType) -> Any:
        """Invoke a method on an object, and return the parsed response.

        Args:
            method: The method to invoke.
            params: The parameters to send with the method.

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
        signature = self.method_signatures[method]

        # Invoke the method
        return await self.command_client.invoke(vid, method, *params, as_type=signature)

    async def fetch_state(self, fields: Sequence[str] | None = None) -> list[str]:
        """Fetch state properties provided by the interface(s) this object implements.

        Args:
            fields: An optional list of fields to fetch, or None to fetch all.
        """
        cls = type(self)

        # Allow fetching a subset of state properties
        fields_to_fetch = [
            field
            for field in cls.property_getters.keys()
            if fields is None or field in fields
        ]

        # Fetch each state property
        attrs_changed: list[str] = []
        for field in fields_to_fetch:
            if getter := cls.property_getters.get(field):
                # Call the getter function
                try:
                    result = await getter(self)
                except NotImplementedError:
                    continue

                # Update the attribute if the result has changed
                if getattr(self, field) != result:
                    setattr(self, field, result)
                    attrs_changed.append(field)

        return attrs_changed
