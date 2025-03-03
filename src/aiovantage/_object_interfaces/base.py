from collections.abc import Callable
from dataclasses import fields, is_dataclass
from typing import (
    Any,
    ClassVar,
    Protocol,
    TypeVar,
    get_type_hints,
    overload,
    runtime_checkable,
)

from aiovantage.command_client import CommandClient, Converter
from aiovantage.errors import CommandError

T = TypeVar("T")


class _AsyncCallable(Protocol):
    async def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


@runtime_checkable
class _MethodCallable(Protocol):
    method_metadata: list[tuple[str, str | None, str | None, bool]]

    async def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


def method(
    *methods: str,
    out: str | None = None,
    property: str | None = None,
    fetch: bool = True,
) -> Callable[[T], T]:
    """Decorator to annotate a function as a Vantage method.

    This is used to automatically keep track of expected return types for
    Vantage method calls so we can parse responses correctly, both when
    directly invoking methods and when receiving status messages.

    Optionally, a property name can be associated with the method, which can
    be used to update the state of the object when receiving status messages,
    or to fetch the initial state of the object.

    Args:
        methods: The vantage method name(s) to associate with the function.
        out: Optional source of the return value, either "return" or "argN".
        property: Optional property name to associate with the function.
        fetch: Whether to fetch the property when fetching state.
    """

    def decorator(func: T) -> T:
        # Attach metadata to the function
        metadata: list[tuple[str, str | None, str | None, bool]] = getattr(
            func, "method_metadata", []
        )

        for method in methods:
            metadata.append((method, out, property, fetch))

        func.method_metadata = metadata  # type: ignore

        return func

    return decorator


class _InterfaceMeta(type):
    """Metaclass to collect method metadata from member functions and base classes."""

    def __new__(
        cls: type["_InterfaceMeta"],
        name: str,
        bases: tuple[type, ...],
        dct: dict[str, Any],
    ):
        """Create a new object interface class."""
        method_signatures: dict[str, type[Any]] = {}
        method_output: dict[str, str] = {}
        method_properties: dict[str, str] = {}
        property_getters: dict[str, _AsyncCallable] = {}

        # Include method metadata from base classes
        for base in bases:
            if issubclass(base, Interface):
                method_signatures.update(base._method_signatures)  # type: ignore
                method_output.update(base._method_output)  # type: ignore
                method_properties.update(base._method_properties)  # type: ignore
                property_getters.update(base._property_getters)  # type: ignore

        # Collect method metadata from member functions
        for attr in dct.values():
            if not isinstance(attr, _MethodCallable):
                continue

            for method, output, property, fetch in attr.method_metadata:
                # Get the return type of the method
                type_hints = get_type_hints(attr)
                if "return" not in type_hints:
                    raise NotImplementedError(f"Return type missing for {method}")

                # Get the fully-qualified method name
                fq_method = f"{dct['interface_name']}.{method}"

                # Save mapping between method name and return type
                # Used for parsing responses
                method_signatures[fq_method] = type_hints["return"]

                # Save mapping between method name and output argument
                # Used for parsing responses
                if output:
                    method_output[fq_method] = output

                # Save mapping between method name and property name
                # Used to update properties when receiving status messages
                if property:
                    method_properties[fq_method] = property

                # Save mapping between property name and getter function
                # Used to fetch state properties
                if property and fetch:
                    property_getters[property] = attr

        # Attach the method metadata to the class
        dct["_method_signatures"] = method_signatures
        dct["_method_output"] = method_output
        dct["_method_properties"] = method_properties
        dct["_property_getters"] = property_getters

        return super().__new__(cls, name, bases, dct)


class Interface(metaclass=_InterfaceMeta):
    """Base class for object interfaces."""

    interface_name: ClassVar[str]
    """The name of the interface."""

    command_client: CommandClient | None = None
    """The command client instance to use for making requests."""

    vid: int
    """The Vantage ID of the object to send requests to, typically set in a subclass."""

    # Method metadata
    _method_signatures: dict[str, type[Any]]
    _method_output: dict[str, str]
    _method_properties: dict[str, str]
    _property_getters: dict[str, _AsyncCallable]

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
        if not self.command_client:
            raise ValueError("The object has no command client to send requests with.")

        # Build the request
        request = f"INVOKE {self.vid} {method}"
        if params:
            request += " " + " ".join(Converter.serialize(p) for p in params)

        # Send the request
        response = await self.command_client.raw_request(request)

        # Break the response into tokens
        return_line = response[-1]
        _command, _vid, result, _method, *args = Converter.tokenize(return_line)

        # Parse the response
        return self._parse_object_response(method, result, *args, as_type=as_type)

    def update_properties(self, properties: dict[str, Any]) -> list[str]:
        """Update object properties.

        Args:
            properties: A dictionary of property names and their new values.

        Returns:
            A list of property names that were updated.
        """
        changed: list[str] = []
        for prop, value in properties.items():
            if hasattr(self, prop) and getattr(self, prop) != value:
                setattr(self, prop, value)
                changed.append(prop)

        return changed

    async def fetch_state(self) -> list[str]:
        """Fetch state properties provided by the interface(s) this object implements.

        Returns:
            A list of property names that were updated.
        """
        # Fetch each state property
        fetched_properties: dict[str, Any] = {}
        for prop, getter in self._property_getters.items():
            try:
                fetched_properties[prop] = await getter(self)
            except CommandError:
                continue

        return self.update_properties(fetched_properties)

    def handle_object_status(self, method: str, result: str, *args: str) -> list[str]:
        """Handle an object interface status message.

        Args:
            method: The method that was invoked.
            result: The result of the command.
            args: The arguments that were sent with the command.

        Returns:
            A list of property names that were updated.
        """
        # Look up the property associated with this method
        property = self._method_properties.get(method)
        if property is None:
            return []

        # Parse the response and update the property
        return self.update_properties(
            {property: self._parse_object_response(method, result, *args)}
        )

    def handle_category_status(self, category: str, *args: str) -> list[str]:
        """Handle category status messages.

        Object interfaces which can handle "legacy" status messages from the
        Host Command service should override this method.

        Args:
            category: The category of the status message, eg. "LOAD".
            args: The arguments that were sent with the command.

        Returns:
            A list of property names that were updated.
        """
        return []

    @classmethod
    def _parse_object_response(
        cls, method: str, result: str, *args: str, as_type: type[T] | None = None
    ) -> T | Any:
        # Parse an object interface response message, either from the response
        # to an INVOKE command, or from a status message.

        # -> R:INVOKE <id> <result> <method> <arg1> <arg2> ...
        # -> EL: <id> <method> <result> <arg1> <arg2> ...
        # -> S:STATUS <id> <method> <result> <arg1> <arg2> ...

        # Make sure we have a signature for the method
        if as_type is None and method not in cls._method_signatures:
            raise NotImplementedError(f"No signature found for method {method}")

        # Get the expected return type of the method, return early if None
        signature = as_type or cls._method_signatures[method]
        if signature in (None, type(None)):
            return None

        # Grab either the result or an argument based on "out" metadata field
        def get_output_value(out: str) -> Any:
            if out == "return":
                return result

            if out.startswith("arg") and out[3:].isdigit():
                index = int(out[3:])
                if 0 <= index < len(args):
                    return args[index]

            raise ValueError(f"Invalid 'out' metadata when parsing {method}")

        # Parse the response based on the expected return type
        if is_dataclass(signature):
            # If the method returns a dataclass, parse the result and/or arguments
            # into the expected fields of the dataclass, based on the field metadata.
            type_hints = get_type_hints(signature)
            props: dict[str, Any] = {}

            for field in fields(signature):
                out = field.metadata.get("out")
                if out is None:
                    raise ValueError(f"Field {field.name} missing 'out' metadata")

                field_signature = type_hints.get(field.name)
                if field_signature is None:
                    raise ValueError(f"Field {field.name} missing type hint")

                props[field.name] = Converter.deserialize(
                    field_signature, get_output_value(out)
                )

            return signature(**props)
        else:
            # Otherwise, parse the result into the expected type
            out = cls._method_output.get(method, "return")
            return Converter.deserialize(signature, get_output_value(out))
