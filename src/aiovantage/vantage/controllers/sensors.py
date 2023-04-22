from typing import Sequence

from typing_extensions import override

from aiovantage.aci_client.system_objects import (
    AnemoSensor,
    LightSensor,
    OmniSensor,
    Sensor,
    Temperature,
)
from aiovantage.vantage.controllers.base import StatefulController


class SensorsController(StatefulController[Sensor]):
    item_cls = Sensor
    vantage_types = (AnemoSensor, LightSensor, OmniSensor, Temperature)
    status_types = ("TEMP", "POWER", "CURRENT")

    @override
    async def fetch_initial_state(self, id: int) -> None:
        ...

    @override
    def handle_state_change(self, id: int, status: str, args: Sequence[str]) -> None:
        ...
