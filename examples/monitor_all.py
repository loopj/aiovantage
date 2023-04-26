import asyncio
import os
from typing import Any, Dict

from aiovantage import Vantage
from aiovantage.aci_client.system_objects import SystemObject
from aiovantage.vantage.controllers.base import EventType

# Set your Vantage host ip, username, and password as environment variables
VANTAGE_HOST = os.getenv("VANTAGE_HOST", "vantage.local")
VANTAGE_USER = os.getenv("VANTAGE_USER")
VANTAGE_PASS = os.getenv("VANTAGE_PASS")


def callback(event: EventType, obj: SystemObject, user_data: Dict[str, Any]) -> None:
    object_type = type(obj).__name__

    if event == EventType.OBJECT_ADDED:
        print(f"[{object_type} added] '{obj.name}' ({obj.id})")

    if event == EventType.OBJECT_UPDATED:
        print(f"[{object_type} updated] '{obj.name}' ({obj.id})")
        for attr in user_data.get("attrs_changed", []):
            print(f"    {attr} = {getattr(obj, attr)}")


async def main() -> None:
    async with Vantage(VANTAGE_HOST, VANTAGE_USER, VANTAGE_PASS) as vantage:
        # Fetch all known objects from the controller and subscribe to updates
        vantage.subscribe(callback)
        await vantage.initialize()

        # Keep running for a while
        await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
