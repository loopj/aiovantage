import asyncio
from typing import Sequence

from aiovantage.aci_client.system_objects import (
    AnemoSensor,
    LightSensor,
    OmniSensor,
    Sensor,
    Temperature,
)
from aiovantage.hc_client import StatusType
from aiovantage.vantage.controllers.base import BaseController


class SensorsController(BaseController[Sensor]):
    item_cls = Sensor
    vantage_types = (AnemoSensor, LightSensor, OmniSensor, Temperature)
    status_types = (
        StatusType.TEMP,
        StatusType.POWER,
        StatusType.CURRENT,
    )

    def _update_object_state(self, vid: int, args: Sequence[str]) -> None:
        # Update the state of a single Sensor.
        ...

    async def _fetch_object_state(self, vid: int) -> None:
        # Fetch initial state of a single Sensor.
        ...

    async def _fetch_initial_states(self) -> None:
        # Fetch initial state of all Sensor.
        await asyncio.gather(*[self._fetch_object_state(obj.id) for obj in self])
