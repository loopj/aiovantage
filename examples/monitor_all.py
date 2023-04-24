import asyncio
import logging
from typing import Any

from aiovantage import Vantage
from aiovantage.vantage.controllers.base import EventType
from aiovantage.aci_client.system_objects import SystemObject

logging.basicConfig(level=logging.INFO)


# This callback will be called whenever an object is updated
def event_callback(event_type: EventType, obj: SystemObject, **kwargs: Any) -> None:
    # Print which object was updated
    print(f"[{event_type.name} {type(obj).__name__}] '{obj.name}' ({obj.id})")

    # Print which attributes were updated
    if "attrs_changed" in kwargs:
        for attr in kwargs["attrs_changed"]:
            print(f"    {attr} = {getattr(obj, attr)}")


async def main() -> None:
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        # Subscribe to status updates for all objects
        vantage.subscribe(event_callback)

        # Fetch all objects from the controller
        await vantage.initialize()

        # Keep running for a while
        await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
