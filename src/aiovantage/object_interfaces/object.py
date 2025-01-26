"""Interface for querying and controlling system objects."""

from dataclasses import dataclass

from .base import Interface


class ObjectInterface(Interface):
    """Interface for querying and controlling system objects."""

    @dataclass
    class PropertyEx:
        """Extended property information."""

        rcode: int
        property: str
        value: str
        size: int

    method_signatures = {
        "Object.GetVID": int,
        "Object.GetController": int,
        "Object.GetType": str,
        "Object.GetName": str,
        "Object.GetModel": str,
        "Object.GetNote": str,
        "Object.GetProperty": int,
        "Object.GetPropertyEx": PropertyEx,
        "Object.IsLocked": bool,
        "Object.IsInterfaceSupported": bool,
        "Object.IsMethodSupported": bool,
        "Object.GetMTime": int,
        "Object.GetDName": str,
        "Object.GetArea": int,
    }

    async def get_vid(self, vid: int) -> int:
        """Get the Vantage ID of an object.

        Args:
            vid: The Vantage ID of the object.

        Returns:
            The Vantage ID of the object.
        """
        # INVOKE <id> Object.GetVID
        # -> R:INVOKE <id> <vid> Object.GetVID
        return await self.invoke(vid, "Object.GetVID")

    async def get_controller(self, vid: int) -> int:
        """Get the VID of the controller of an object.

        Args:
            vid: The Vantage ID of the object.

        Returns:
            The VID of the controller of the object.
        """
        # INVOKE <id> Object.GetController
        # -> R:INVOKE <id> <controller> Object.GetController
        return await self.invoke(vid, "Object.GetController")

    async def get_type(self, vid: int) -> str:
        """Get the type of an object.

        Args:
            vid: The Vantage ID of the object.

        Returns:
            The type of the object.
        """
        # INVOKE <id> Object.GetType
        # -> R:INVOKE <id> <type> Object.GetType
        return await self.invoke(vid, "Object.GetType")

    async def get_name(self, vid: int) -> str:
        """Get the name field of an object.

        Args:
            vid: The Vantage ID of the object.

        Returns:
            The name of the object.
        """
        # INVOKE <id> Object.GetName
        # -> R:INVOKE <id> <name> Object.GetName
        return await self.invoke(vid, "Object.GetName")

    async def get_model(self, vid: int) -> str:
        """Get the model field of an object.

        Args:
            vid: The Vantage ID of the object.

        Returns:
            The model of the object.
        """
        # INVOKE <id> Object.GetModel
        # -> R:INVOKE <id> <model> Object.GetModel
        return await self.invoke(vid, "Object.GetModel")

    async def get_note(self, vid: int) -> str:
        """Get the note field of an object.

        Args:
            vid: The Vantage ID of the object.

        Returns:
            The note of the object.
        """
        # INVOKE <id> Object.GetNote
        # -> R:INVOKE <id> <note> Object.GetNote
        return await self.invoke(vid, "Object.GetNote")

    async def get_property(self, vid: int, xpath: str) -> int:
        """Get an integer property of an object.

        Args:
            vid: The Vantage ID of the object.
            xpath: XPath of the property to get, eg: "DName", "Get/Formula/@ReturnType, etc.

        Returns:
            The value of the property.
        """
        # INVOKE <id> Object.GetProperty <xpath>
        # -> R:INVOKE <id> <value> Object.GetProperty <xpath>
        return await self.invoke(vid, "Object.GetProperty", xpath)

    async def get_property_ex(self, vid: int, xpath: str) -> PropertyEx:
        """Get a string property of an object.

        Args:
            vid: The Vantage ID of the object.
            xpath: XPath of the property to get, eg: "DName", "Get/Formula/@ReturnType, etc.

        Returns:
            The value of the property.
        """
        # INVOKE <id> Object.GetPropertyEx <xpath>
        # -> R:INVOKE <id> <value> Object.GetPropertyEx <xpath>
        return await self.invoke(vid, "Object.GetPropertyEx", xpath)

    async def lock(self, vid: int) -> None:
        """Lock an object.

        Args:
            vid: The Vantage ID of the object.
        """
        # INVOKE <id> Object.Lock
        # -> R:INVOKE <id> <rcode> Object.Lock
        await self.invoke(vid, "Object.Lock")

    async def unlock(self, vid: int) -> None:
        """Unlock an object.

        Args:
            vid: The Vantage ID of the object.
        """
        # INVOKE <id> Object.Unlock
        # -> R:INVOKE <id> <rcode> Object.Unlock
        await self.invoke(vid, "Object.Unlock")

    async def is_locked(self, vid: int) -> bool:
        """Check if an object is locked.

        Args:
            vid: The Vantage ID of the object.

        Returns:
            True if the object is locked, False otherwise.
        """
        # INVOKE <id> Object.IsLocked
        # -> R:INVOKE <id> <locked (0/1)> Object.IsLocked
        return await self.invoke(vid, "Object.IsLocked")

    async def is_interface_supported(self, vid: int, iid: int) -> bool:
        """Check if an interface is supported by an object.

        Args:
            vid: The Vantage ID of the object.
            iid: The interface ID to check.

        Returns:
            True if the interface is supported, False otherwise.
        """
        # INVOKE <id> Object.IsInterfaceSupported <iid>
        # -> R:INVOKE <id> <supported (0/1)> Object.IsInterfaceSupported <iid>
        return await self.invoke(vid, "Object.IsInterfaceSupported", iid)

    async def is_method_supported(self, vid: int, iid: int, mid: int) -> bool:
        """Check if a method is supported by an object.

        Args:
            vid: The Vantage ID of the object.
            iid: The interface ID to check.
            mid: The method ID to check.

        Returns:
            True if the method is supported, False otherwise.
        """
        # INVOKE <id> Object.IsMethodSupported <iid> <mid>
        # -> R:INVOKE <id> <supported (0/1)> Object.IsMethodSupported <iid> <mid>
        return await self.invoke(vid, "Object.IsMethodSupported", iid, mid)

    async def set_property(self, vid: int, property: str, value: int) -> None:
        """Set an integer property of an object.

        Args:
            vid: The Vantage ID of the object.
            property: The property to set.
            value: The value to set the property to.
        """
        # INVOKE <id> Object.SetProperty <property> <value>
        # -> R:INVOKE <id> <rcode> Object.SetProperty <property> <value>
        await self.invoke(vid, "Object.SetProperty", property, value)

    async def set_property_ex(self, vid: int, property: str, value: str) -> None:
        """Set a string property of an object.

        Args:
            vid: The Vantage ID of the object.
            property: The property to set.
            value: The value to set the property to.
        """
        # INVOKE <id> Object.SetPropertyEx <property> <value>
        # -> R:INVOKE <id> <rcode> Object.SetPropertyEx <property> <value>
        await self.invoke(vid, "Object.SetPropertyEx", property, value)

    async def get_mtime(self, vid: int) -> int:
        """Get the modification time of an object.

        Args:
            vid: The Vantage ID of the object.

        Returns:
            The modification time of the object, as a unix timestamp.
        """
        # INVOKE <id> Object.GetMTime
        # -> R:INVOKE <id> <mtime> Object.GetMTime
        return await self.invoke(vid, "Object.GetMTime")

    async def get_dname(self, vid: int) -> str:
        """Get the display name of an object.

        Args:
            vid: The Vantage ID of the object.

        Returns:
            The display name of the object.
        """
        # INVOKE <id> Object.GetDName
        # -> R:INVOKE <id> <dname> Object.GetDName
        return await self.invoke(vid, "Object.GetDName")

    async def get_area(self, vid: int) -> int:
        """Get the area of an object.

        Args:
            vid: The Vantage ID of the object.

        Returns:
            The area of the object.
        """
        # INVOKE <id> Object.GetArea
        # -> R:INVOKE <id> <area> Object.GetArea
        return await self.invoke(vid, "Object.GetArea")
