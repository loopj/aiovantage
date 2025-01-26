"""Interface for controller configuration."""

from enum import IntEnum, IntFlag

from .base import Interface


class ConfigurationInterface(Interface):
    """Interface for controller introspection."""

    class Store(IntEnum):
        """Configuration store."""

        Unspecified = 0
        Datastore = 1
        Userstore = 2

    class Compression(IntFlag):
        """Configuration compression type."""

        none = 1
        zlib = 2
        snappy = 4

    class SolarEvent(IntEnum):
        """Solar event types."""

        Sunrise = 0
        Sunset = 1

    method_signatures = {
        "Configuration.GetControllerVID": int,
        "Configuration.CreateObject": int,
        "Configuration.GetModificationTime": int,
        "Configuration.GetLastDeleteTime": int,
        "Configuration.GetLastClearTime": int,
        "Configuration.OpenFilter": int,
        "Configuration.GetNextObjectVID": int,
        "Configuration.FindLocalObject": bool,
        "Configuration.GetTimeZone": str,
        "Configuration.GetTimeLocation": str,
        "Configuration.GetAstronomicalTime": int,
    }

    async def get_controller_vid(self, vid: int, controller: int) -> int:
        """Get the VID of a controller, based on the controller number.

        Args:
            vid: The VID of the controller.
            controller: The controller number to get the VID of.
        """
        # INVOKE <id> Configuration.GetControllerVID <controller>
        # -> R:INVOKE <id> <rcode> Configuration.GetControllerVID <vid>
        return await self.invoke(vid, "Configuration.GetControllerVID", controller)

    async def delete_object(self, vid: int, store: Store, object_vid: int) -> None:
        """Delete an object from the controller.

        Args:
            vid: The VID of the controller
            store: The store to delete the object from.
            object_vid: The VID of the object to delete.
        """
        # INVOKE <id> Configuration.DeleteObject <vid>
        # -> R:INVOKE <id> <rcode> Configuration.DeleteObject <vid>
        await self.invoke(vid, "Configuration.DeleteObject", store, object_vid)

    async def create_object(self, vid: int, type: str) -> int:
        """Create an object on the controller.

        Args:
            vid: The VID of the controller.
            type: The type of object to create, eg. "Load".

        Returns:
            The VID of the created object, 0 if the object could not be created.
        """
        # INVOKE <id> Configuration.CreateObject <type>
        # -> R:INVOKE <id> <rcode> Configuration.CreateObject <type>
        return await self.invoke(vid, "Configuration.CreateObject", type)

    async def get_modification_time(self, vid: int) -> int:
        """Get the modification time of this object.

        Args:
            vid: The VID of the object.

        Returns:
            The modification time of the object, as a timestamp.
        """
        # INVOKE <id> Configuration.GetModificationTime
        # -> R:INVOKE <id> <mtime> Configuration.GetModificationTime
        return await self.invoke(vid, "Configuration.GetModificationTime")

    async def get_last_delete_time(self, vid: int, store: Store) -> int:
        """Get the time of the last object deletion.

        Args:
            vid: The VID of the controller.
            store: The store to get the last deletion time of.

        Returns:
            The time of the last object deletion, as a timestamp.
        """
        # INVOKE <id> Configuration.GetLastDeleteTime <store>
        # -> R:INVOKE <id> <time> Configuration.GetLastDeleteTime <store>
        return await self.invoke(vid, "Configuration.GetLastDeleteTime", store)

    async def get_last_clear_time(self, vid: int) -> int:
        """Get the time of the last clear.

        Args:
            vid: The VID of the controller.

        Returns:
            The time of the last store clear, as a datetime object.
        """
        # INVOKE <id> Configuration.GetLastClearTime
        # -> R:INVOKE <id> <time> Configuration.GetLastClearTime
        return await self.invoke(vid, "Configuration.GetLastClearTime")

    async def open_filter(
        self, vid: int, store: Store, types: str = "", xpath: str = ""
    ) -> int:
        """Open a filter on a store.

        Args:
            vid: The VID of the controller.
            store: The store to open the filter on.
            types: An optional comma-separated list of object types to filter on.
            xpath: An optional xpath expression to filter on, eg. "/Load", "/*[@VID='12']"

        Returns:
            An integer "handle" representing the opened filter.
        """
        # INVOKE <id> Configuration.OpenFilter <store> <types> <xpath>
        # -> R:INVOKE <id> <handle> Configuration.OpenFilter <store> <types> <xpath>
        return await self.invoke(vid, "Configuration.OpenFilter", store, types, xpath)

    async def get_next_object_vid(self, vid: int, handle: int) -> int:
        """Get the VID of the next object in a filter.

        Args:
            vid: The VID of the controller.
            handle: The filter handle to get the next object of.

        Returns:
            The VID of the next object in the filter, or 0 if there are no more objects.
        """
        # INVOKE <id> Configuration.GetNextObjectVID <handle>
        # -> R:INVOKE <id> <vid> Configuration.GetNextObjectVID <handle>
        return await self.invoke(vid, "Configuration.GetNextObjectVID", handle)

    async def close_filter(self, vid: int, handle: int) -> None:
        """Close a filter.

        Args:
            vid: The VID of the controller.
            handle: The filter handle to close.
        """
        # INVOKE <id> Configuration.CloseFilter <handle>
        # -> R:INVOKE <id> <rcode> Configuration.CloseFilter <handle>
        await self.invoke(vid, "Configuration.CloseFilter", handle)

    async def find_local_object(self, vid: int) -> bool:
        """Find a "local" object by VID, i.e. an object managed by this object.

        Args:
            vid: The VID of the object to find.

        Returns:
            True if the object is found, False otherwise.
        """
        # INVOKE <id> Configuration.FindLocalObject <vid>
        # -> R:INVOKE <id> <found (0/1)> Configuration.FindLocalObject <vid>
        return await self.invoke(vid, "Configuration.FindLocalObject", vid)

    async def get_time_zone(self, vid: int) -> str:
        """Get the time zone.

        Args:
            vid: The VID of the controller

        Returns:
            The vantage time zone string, eg. "UTCPlusEight+8DAY,M3.2.0/02:00,M11.1.0/02:00"
        """
        # INVOKE <id> Configuration.GetTimeZone
        # -> R:INVOKE <id> <rcode> Configuration.GetTimeZone <tz> <size>
        return await self.invoke(vid, "Configuration.GetTimeZone")

    async def get_time_location(self, vid: int) -> str:
        """Get the time location.

        Args:
            vid: The VID of the controller

        Returns:
            A latitude and longitude string, eg. "51.178908N1.826212W"
        """
        # INVOKE <id> Configuration.GetTimeLocation
        # -> R:INVOKE <id> <rcode> Configuration.GetTimeLocation <loc> <size>
        return await self.invoke(vid, "Configuration.GetTimeLocation")

    async def get_astronomical_time(
        self, vid: int, event: SolarEvent, year: int, month: int, day: int
    ) -> int:
        """Get the astronomical time of a solar event.

        Args:
            vid: The VID of the controller.
            event: The solar event to get the time of.
            year: The year of the event.
            month: The month of the event.
            day: The day of the event.

        Returns:
            The time of the solar event, as a datetime object.
        """
        # INVOKE <id> Configuration.GetAstronomicalTime <event>
        # -> R:INVOKE <id> <time> Configuration.GetAstronomicalTime <event> <year> <month> <day>
        return await self.invoke(
            vid, "Configuration.GetAstronomicalTime", event, year, month, day
        )
