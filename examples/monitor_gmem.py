import asyncio
import os
from typing import Any, Dict

from aiovantage import Vantage
from aiovantage.aci_client.system_objects import GMem
from aiovantage.vantage.controllers.base import EventType

# Set your Vantage host ip, username, and password as environment variables
VANTAGE_HOST = os.getenv("VANTAGE_HOST", "vantage.local")
VANTAGE_USER = os.getenv("VANTAGE_USER")
VANTAGE_PASS = os.getenv("VANTAGE_PASS")


def callback(event: EventType, obj: GMem, user_data: Dict[str, Any]) -> None:
    if event == EventType.OBJECT_ADDED:
        print(f"[GMem added] '{obj.name}' ({obj.id})")

    if event == EventType.OBJECT_UPDATED:
        print(f"[GMem updated] '{obj.name}' ({obj.id})")
        for attr in user_data.get("attrs_changed", []):
            print(f"    {attr} = {getattr(obj, attr)}")


async def main() -> None:
    async with Vantage(VANTAGE_HOST, VANTAGE_USER, VANTAGE_PASS) as vantage:
        # Fetch all known GMem objects from the controller and subscribe to updates
        vantage.gmem.subscribe(callback)
        await vantage.gmem.initialize()

        # Keep running for a while
        await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
