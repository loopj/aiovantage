"""Interface for querying and controlling system objects."""

import datetime as dt
from typing import NamedTuple

from .base import Interface, method


class ObjectInterface(Interface):
    """Interface for querying and controlling system objects."""

    class PropertyExResponse(NamedTuple):
        """Response from Object.GetPropertyEx."""

        rcode: int
        property: str
        value: str
        size: int

    @method("Object.GetVID")
    async def get_vid(self) -> int:
        """Get the Vantage ID of an object.

        Returns:
            The Vantage ID of the object.
        """
        # INVOKE <id> Object.GetVID
        # -> R:INVOKE <id> <vid> Object.GetVID
        return await self.invoke("Object.GetVID")

    @method("Object.GetController")
    async def get_controller(self) -> int:
        """Get the VID of the controller of an object.

        Returns:
            The VID of the controller of the object.
        """
        # INVOKE <id> Object.GetController
        # -> R:INVOKE <id> <controller> Object.GetController
        return await self.invoke("Object.GetController")

    @method("Object.GetType")
    async def get_type(self) -> str:
        """Get the type of an object.

        Returns:
            The type of the object.
        """
        # INVOKE <id> Object.GetType
        # -> R:INVOKE <id> <type> Object.GetType
        return await self.invoke("Object.GetType")

    @method("Object.GetName")
    async def get_name(self) -> str:
        """Get the name field of an object.

        Returns:
            The name of the object.
        """
        # INVOKE <id> Object.GetName
        # -> R:INVOKE <id> <name> Object.GetName
        return await self.invoke("Object.GetName")

    @method("Object.GetModel")
    async def get_model(self) -> str:
        """Get the model field of an object.

        Returns:
            The model of the object.
        """
        # INVOKE <id> Object.GetModel
        # -> R:INVOKE <id> <model> Object.GetModel
        return await self.invoke("Object.GetModel")

    @method("Object.GetNote")
    async def get_note(self) -> str:
        """Get the note field of an object.

        Returns:
            The note of the object.
        """
        # INVOKE <id> Object.GetNote
        # -> R:INVOKE <id> <note> Object.GetNote
        return await self.invoke("Object.GetNote")

    @method("Object.GetProperty")
    async def get_property(self, property: str) -> int:
        """Get an integer property of an object.

        Args:
            property: The property to get.

        Returns:
            The value of the property.
        """
        # INVOKE <id> Object.GetProperty <property>
        # -> R:INVOKE <id> <value> Object.GetProperty <property>
        return await self.invoke("Object.GetProperty", property)

    @method("Object.GetPropertyEx")
    async def get_property_ex(self, property: str) -> PropertyExResponse:
        """Get a string property of an object.

        Args:
            property: The property to get.

        Returns:
            The value of the property.
        """
        # INVOKE <id> Object.GetPropertyEx <property>
        # -> R:INVOKE <id> <value> Object.GetPropertyEx <property>
        return await self.invoke("Object.GetPropertyEx", property)

    @method("Object.Lock")
    async def lock(self) -> None:
        """Lock an object."""
        # INVOKE <id> Object.Lock
        # -> R:INVOKE <id> <rcode> Object.Lock
        await self.invoke("Object.Lock")

    @method("Object.Unlock")
    async def unlock(self) -> None:
        """Unlock an object."""
        # INVOKE <id> Object.Unlock
        # -> R:INVOKE <id> <rcode> Object.Unlock
        await self.invoke("Object.Unlock")

    @method("Object.IsLocked")
    async def is_locked(self) -> bool:
        """Check if an object is locked.

        Returns:
            True if the object is locked, False otherwise.
        """
        # INVOKE <id> Object.IsLocked
        # -> R:INVOKE <id> <locked (0/1)> Object.IsLocked
        return await self.invoke("Object.IsLocked")

    @method("Object.GetMTime")
    async def get_mtime(self) -> dt.datetime:
        """Get the modification time of an object.

        Returns:
            The modification time of the object, as a unix timestamp.
        """
        # INVOKE <id> Object.GetMTime
        # -> R:INVOKE <id> <mtime> Object.GetMTime
        return await self.invoke("Object.GetMTime")
