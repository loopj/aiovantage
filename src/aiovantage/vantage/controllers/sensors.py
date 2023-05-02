from typing import Sequence

from typing_extensions import override

from aiovantage.config_client.objects import (
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

    @override
    async def fetch_initial_state(self, id: int) -> None:
        ...

    @override
    def handle_state_change(self, id: int, status: str, args: Sequence[str]) -> None:
        ...
