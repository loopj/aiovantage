import asyncio
from types import TracebackType
from typing import Optional, Type

from aiovantage.aci_client import ACIClient
from aiovantage.aci_client.system_objects import SystemObject
from aiovantage.hc_client import HCClient
from aiovantage.controllers.base import EventCallBackType
from aiovantage.controllers.areas import AreasController
from aiovantage.controllers.buttons import ButtonsController
from aiovantage.controllers.dry_contacts import DryContactsController
from aiovantage.controllers.loads import LoadsController
from aiovantage.controllers.sensors import SensorsController
from aiovantage.controllers.stations import StationsController
from aiovantage.controllers.tasks import TasksController


class Vantage:
    """Control a Vantage InFusion controller."""

    def __init__(
        self,
        host: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_ssl: bool = True,
        aci_port: Optional[int] = None,
        hc_port: Optional[int] = None,
    ) -> None:
        """Initialize the Vantage instance."""

        self._aci_client = ACIClient(host, username, password, use_ssl=use_ssl, port=aci_port)
        self._hc_client = HCClient(host, username, password, use_ssl, hc_port)

        self._areas = AreasController(self)
        self._loads = LoadsController(self)
        self._buttons = ButtonsController(self)
        self._dry_contacts = DryContactsController(self)
        self._sensors = SensorsController(self)
        self._tasks = TasksController(self)
        self._stations = StationsController(self)

    async def __aenter__(self) -> "Vantage":
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.close()

    @property
    def areas(self) -> AreasController:
        """Return the Areas controller for managing areas."""
        return self._areas

    @property
    def loads(self) -> LoadsController:
        """Return the Loads controller for managing loads (lights, fans, etc)."""
        return self._loads

    @property
    def stations(self) -> StationsController:
        """Return the Stations controller for managing stations (keypads, etc)."""
        return self._stations

    @property
    def buttons(self) -> ButtonsController:
        """Return the Buttons controller for managing buttons."""
        return self._buttons

    @property
    def dry_contacts(self) -> DryContactsController:
        """Return the DryContacts controller for managing dry contacts (motion sensors, etc)."""
        return self._dry_contacts

    @property
    def sensors(self) -> SensorsController:
        """Return the OmniSensors controller for managing generic sensors."""
        return self._sensors

    @property
    def tasks(self) -> TasksController:
        """Return the Tasks controller for managing tasks."""
        return self._tasks

    async def connect(self) -> None:
        """Initialize the clients."""

        await asyncio.gather(
            self._aci_client.connect(),
            self._hc_client.initialize(),
        )

    async def close(self) -> None:
        """Close the clients."""

        await asyncio.gather(
            self._aci_client.close(),
            self._hc_client.close(),
        )

    async def initialize(self) -> None:
        """Fetch all objects from the controllers."""

        coros = [
            self._areas.initialize(),
            self._loads.initialize(),
            self._stations.initialize(),
            self._buttons.initialize(),
            self._dry_contacts.initialize(),
            self._sensors.initialize(),
            self._tasks.initialize(),
        ]

        # TODO: Connection pool? asyncio.gather?
        for coro in coros:
            await coro

    def subscribe(self, callback: EventCallBackType[SystemObject]) -> None:
        """Subscribe to all controller events."""

        self.areas.subscribe(callback)
        self.loads.subscribe(callback)
        self.stations.subscribe(callback)
        self.buttons.subscribe(callback)
        self.dry_contacts.subscribe(callback)
        self.sensors.subscribe(callback)
        self.tasks.subscribe(callback)