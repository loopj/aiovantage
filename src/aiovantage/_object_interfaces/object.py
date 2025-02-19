import datetime as dt
from enum import IntEnum
from typing import TypeVar

from .base import Interface, method

IntEnumT = TypeVar("IntEnumT", bound=IntEnum)


class ObjectInterface(Interface):
    """'Object' object interface."""

    interface_name = "Object"

    # Properties
    m_time: dt.datetime | None = None

    # Methods
    @method("GetVID")
    async def get_vid(self) -> int:
        """Get the Vantage ID of an object.

        Returns:
            The Vantage ID of the object.
        """
        # INVOKE <id> Object.GetVID
        # -> R:INVOKE <id> <vid> Object.GetVID
        return await self.invoke("Object.GetVID")

    @method("GetController")
    async def get_controller(self) -> int:
        """Get the VID of the controller of an object.

        Returns:
            The VID of the controller of the object.
        """
        # INVOKE <id> Object.GetController
        # -> R:INVOKE <id> <controller> Object.GetController
        return await self.invoke("Object.GetController")

    @method("GetType", out="arg0")
    async def get_type(self) -> str:
        """Get the type of an object.

        Returns:
            The type of the object.
        """
        # INVOKE <id> Object.GetType
        # -> R:INVOKE <id> <type> Object.GetType
        return await self.invoke("Object.GetType")

    @method("GetName", out="arg0")
    async def get_name(self) -> str:
        """Get the name field of an object.

        Returns:
            The name of the object.
        """
        # INVOKE <id> Object.GetName
        # -> R:INVOKE <id> <name> Object.GetName
        return await self.invoke("Object.GetName")

    @method("GetModel", out="arg0")
    async def get_model(self) -> str:
        """Get the model field of an object.

        Returns:
            The model of the object.
        """
        # INVOKE <id> Object.GetModel
        # -> R:INVOKE <id> <model> Object.GetModel
        return await self.invoke("Object.GetModel")

    @method("GetNote", out="arg0")
    async def get_note(self) -> str:
        """Get the note field of an object.

        Returns:
            The note of the object.
        """
        # INVOKE <id> Object.GetNote
        # -> R:INVOKE <id> <note> Object.GetNote
        return await self.invoke("Object.GetNote")

    @method("GetProperty")
    async def get_property(self, xpath: str) -> int:
        """Get an integer property of an object.

        Args:
            xpath: XPath of the property to get, eg: "DName", "Get/Formula/@ReturnType, etc.

        Returns:
            The value of the property.
        """
        # INVOKE <id> Object.GetProperty <xpath>
        # -> R:INVOKE <id> <value> Object.GetProperty <xpath>
        return await self.invoke("Object.GetProperty", xpath)

    @method("GetPropertyEx", out="arg1")
    async def get_property_ex(self, xpath: str) -> str:
        """Get a string property of an object.

        Args:
            xpath: XPath of the property to get, eg: "DName", "Get/Formula/@ReturnType, etc.

        Returns:
            The value of the property.
        """
        # INVOKE <id> Object.GetPropertyEx <xpath>
        # -> R:INVOKE <id> <value> Object.GetPropertyEx <xpath>
        return await self.invoke("Object.GetPropertyEx", xpath)

    @method("Lock")
    async def lock(self) -> None:
        """Lock an object."""
        # INVOKE <id> Object.Lock
        # -> R:INVOKE <id> <rcode> Object.Lock
        await self.invoke("Object.Lock")

    @method("Unlock")
    async def unlock(self) -> None:
        """Unlock an object."""
        # INVOKE <id> Object.Unlock
        # -> R:INVOKE <id> <rcode> Object.Unlock
        await self.invoke("Object.Unlock")

    @method("IsLocked")
    async def is_locked(self) -> bool:
        """Check if an object is locked.

        Returns:
            True if the object is locked, False otherwise.
        """
        # INVOKE <id> Object.IsLocked
        # -> R:INVOKE <id> <locked (0/1)> Object.IsLocked
        return await self.invoke("Object.IsLocked")

    @method("IsInterfaceSupported")
    async def is_interface_supported(self, iid: int) -> bool:
        """Check if an interface is supported by an object.

        Args:
            iid: The interface ID to check.

        Returns:
            True if the interface is supported, False otherwise.
        """
        # INVOKE <id> Object.IsInterfaceSupported <iid>
        # -> R:INVOKE <id> <supported (0/1)> Object.IsInterfaceSupported <iid>
        return await self.invoke("Object.IsInterfaceSupported", iid)

    @method("IsMethodSupported")
    async def is_method_supported(self, iid: int, mid: int) -> bool:
        """Check if a method is supported by an object.

        Args:
            iid: The interface ID to check.
            mid: The method ID to check.

        Returns:
            True if the method is supported, False otherwise.
        """
        # INVOKE <id> Object.IsMethodSupported <iid> <mid>
        # -> R:INVOKE <id> <supported (0/1)> Object.IsMethodSupported <iid> <mid>
        return await self.invoke("Object.IsMethodSupported", iid, mid)

    @method("SetProperty")
    async def set_property(self, property: str, value: int) -> None:
        """Set an integer property of an object.

        Args:
            property: The property to set.
            value: The value to set the property to.
        """
        # INVOKE <id> Object.SetProperty <property> <value>
        # -> R:INVOKE <id> <rcode> Object.SetProperty <property> <value>
        await self.invoke("Object.SetProperty", property, value)

    @method("SetPropertyEx")
    async def set_property_ex(self, property: str, value: str) -> None:
        """Set a string property of an object.

        Args:
            property: The property to set.
            value: The value to set the property to.
        """
        # INVOKE <id> Object.SetPropertyEx <property> <value>
        # -> R:INVOKE <id> <rcode> Object.SetPropertyEx <property> <value>
        await self.invoke("Object.SetPropertyEx", property, value)

    @method("IsEnumeratorSupported")
    async def is_enumerator_supported(
        self, interface_name: str, enumeration_name: str, enumerator_name: str
    ) -> bool:
        """Check if an enumerator is supported by an object.

        Args:
            interface_name: The name of the interface to check.
            enumeration_name: The name of the enumeration to check.
            enumerator_name: The name of the enumerator to check.

        Returns:
            True if the enumerator is supported, False otherwise.
        """
        # INVOKE <id> Object.IsEnumeratorSupported <interfaceName> <enumerationName> <enumeratorName>
        # -> R:INVOKE <id> <supported (0/1)> Object.IsEnumeratorSupported <interfaceName> <enumerationName> <enumeratorName>
        return await self.invoke(
            "Object.IsEnumeratorSupported",
            interface_name,
            enumeration_name,
            enumerator_name,
        )

    @method("GetMTime", property="m_time", fetch=False)
    async def get_m_time(self) -> dt.datetime:
        """Get the modification time of an object.

        Returns:
            The modification time of the object, as a datetime object.
        """
        # INVOKE <id> Object.GetMTime
        # -> R:INVOKE <id> <mtime> Object.GetMTime
        return await self.invoke("Object.GetMTime")

    @method("GetDName", out="arg0")
    async def get_d_name(self) -> str:
        """Get the display name of an object.

        Returns:
            The display name of the object.
        """
        # INVOKE <id> Object.GetDName
        # -> R:INVOKE <id> <dname> Object.GetDName
        return await self.invoke("Object.GetDName")

    @method("GetArea")
    async def get_area(self) -> int:
        """Get the area of an object.

        Returns:
            The area of the object.
        """
        # INVOKE <id> Object.GetArea
        # -> R:INVOKE <id> <area> Object.GetArea
        return await self.invoke("Object.GetArea")

    # Convenience functions, not part of the interface
    async def get_supported_enum_values(
        self, interface: type[Interface], enum: type[IntEnumT]
    ) -> list[IntEnumT]:
        """Get all supported enum values of an object."""
        return [
            val
            for val in enum
            if await self.is_enumerator_supported(
                interface.interface_name, enum.__name__, val.name
            )
        ]
