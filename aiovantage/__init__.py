import asyncio
import logging
from types import TracebackType
from typing import Optional, Type

from .clients.aci import ACIClient
from .clients.hc import HCClient
from .controllers.areas import AreasController
from .controllers.buttons import ButtonsController
from .controllers.dry_contacts import DryContactsController
from .controllers.loads import LoadsController
from .controllers.omni_sensors import OmniSensorsController
from .controllers.stations import StationsController
from .controllers.tasks import TasksController


class Vantage:
    def __init__(
        self,
        host: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_ssl: bool = True,
        aci_port: Optional[int] = None,
        hc_port: Optional[int] = None,
    ) -> None:
        self._aci_client = ACIClient(host, username, password, use_ssl, aci_port)
        self._events_client = HCClient(host, username, password, use_ssl, hc_port)
        self._commands_client = HCClient(host, username, password, use_ssl, hc_port)

        self._logger = logging.getLogger(__name__)

        self._areas = AreasController()
        self._loads = LoadsController()
        self._buttons = ButtonsController()
        self._dry_contacts = DryContactsController()
        self._omni_sensors = OmniSensorsController()
        self._tasks = TasksController()
        self._stations = StationsController()

    async def __aenter__(self) -> "Vantage":
        """Return Context manager."""
        await self.initialize()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Close context manager."""
        await self.close()

    async def initialize(self) -> None:
        # Connect ACI and HC clients
        await asyncio.gather(
            self._aci_client.initialize(),
            self._events_client.initialize(),
            self._commands_client.initialize(),
        )

        # TODO: Concurrency? Lazy loading?
        await self._areas.initialize(self)
        await self._loads.initialize(self)
        await self._stations.initialize(self)
        await self._buttons.initialize(self)
        await self._dry_contacts.initialize(self)
        await self._omni_sensors.initialize(self)
        await self._tasks.initialize(self)

    async def close(self) -> None:
        await asyncio.gather(
            self._aci_client.close(),
            self._events_client.close(),
            self._commands_client.close(),
        )

    @property
    def areas(self) -> AreasController:
        return self._areas

    @property
    def loads(self) -> LoadsController:
        return self._loads

    @property
    def stations(self) -> StationsController:
        return self._stations

    @property
    def buttons(self) -> ButtonsController:
        return self._buttons

    @property
    def dry_contacts(self) -> DryContactsController:
        return self._dry_contacts

    @property
    def omni_sensors(self) -> OmniSensorsController:
        return self._omni_sensors

    @property
    def tasks(self) -> TasksController:
        return self._tasks
