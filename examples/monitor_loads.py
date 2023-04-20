import asyncio
import logging
from typing import Any, Union

from aiovantage import Vantage
from aiovantage.aci_client.system_objects import Load, RGBLoad

logging.basicConfig(level=logging.INFO)


# This callback will be called whenever a load is updated
def event_callback(obj: Union[Load, RGBLoad], args: Any) -> None:
    print(f"{obj.name} changed level to {obj.level}%")


async def main() -> None:
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        # Fetch all known loads from the controller
        await vantage.loads.initialize()
        await vantage.rgb_loads.initialize()

        # Subscribe to status updates for all loads
        vantage.loads.subscribe(event_callback)
        vantage.rgb_loads.subscribe(event_callback)

        # Keep running for a while
        await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
