import asyncio
import logging

from aiovantage import Vantage

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        await vantage.areas.initialize()
        await vantage.loads.initialize()

        while True:
            for load in vantage.loads.on():
                area = vantage.areas.get(load.area) if load.area else None
                print(f"{load.name} ({area.name if area else 'Unknown Area'})")
            print()

            await asyncio.sleep(5)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
