"""Base class for command client interfaces."""

from collections.abc import Sequence
from types import NoneType
from typing import Any, TypeVar, get_type_hints, overload

from aiovantage.command_client import CommandClient
from aiovantage.command_client.utils import (
    ParameterType,
    encode_params,
    parse_param,
    tokenize_response,
)
from aiovantage.errors import NotImplementedError

T = TypeVar("T")


def method(method: str, *, property: str | None = None):
    """Decorator to map a python function to a Vantage method.

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

    def decorator(func):
        func._method = method
        func._property = property
        func._return_type = get_type_hints(func).get("return")

        return func

    return decorator


class InterfaceMeta(type):
    """Metaclass for object interfaces."""

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

        # Include method signatures from base classes
        for base in bases:
            if hasattr(base, "method_signatures"):
                cls_obj.method_signatures.update(base.method_signatures)

            if hasattr(base, "property_getters"):
                cls_obj.property_getters.update(base.property_getters)

        # Collect method signatures
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

    @overload
    async def invoke(self, method: str, *params: ParameterType) -> Any: ...

    @overload
    async def invoke(
        self, method: str, *params: ParameterType, as_type: type[T]
    ) -> T: ...

    async def invoke(
        self,
        method: str,
        *params: ParameterType,
        as_type: type[T] | None = None,
        vid: int | None = None,
    ) -> T | Any | None:
        """Invoke a method on an object, and return the parsed response.

        Args:
            method: The method to invoke.
            params: The parameters to send with the method.
            as_type: The type to cast the response to.
            vid: Specify the vid of the object to invoke the method on.

        Returns:
            A parsed response, or None if no response was expected.
        """
        # Make sure we have a vid to invoke the method on
        vid = vid or getattr(self, "vid", None)
        if vid is None:
            raise ValueError("The object must have a vid attribute to invoke methods.")

        # Make sure we have a command client to send requests with
        if self.command_client is None:
            raise ValueError("The object has no command client to send requests with.")

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
    ) -> T: ...

    @overload
    @classmethod
    def parse_response(cls, method: str, result: str, *args: str) -> Any: ...

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
        if signature is NoneType:
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
    def _get_signature(cls, method: str) -> type:
        # Get the signature of a method.
        for klass in cls.__mro__:
            if issubclass(klass, Interface) and method in klass.method_signatures:
                return klass.method_signatures[method]

        raise ValueError(f"No signature found for method '{method}'.")

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
