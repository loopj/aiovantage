import asyncio
import logging

from typing import Dict

from .controllers import (LoadsController, AreasController,
                          DryContactsController, OmniSensorsController,
                          ButtonsController, TasksController,
                          StationsController)
from .aci_client import ACIClient
from .hc_client import HCClient

class Vantage:
    def __init__(self, host, username = None, password = None,
                 use_ssl = True, aci_port = None, hc_port = None):
        self._aci_client = ACIClient(host, username, password, use_ssl, aci_port)
        self._hc_client = HCClient(host, username, password, use_ssl, hc_port)

        self._logger = logging.getLogger(__name__)

        self._areas = AreasController(self)
        self._loads = LoadsController(self)
        self._buttons = ButtonsController(self)
        self._dry_contacts = DryContactsController(self)
        self._omni_sensors = OmniSensorsController(self)
        self._tasks = TasksController(self)
        self._stations = StationsController(self)

    async def __aenter__(self):
        """Return Context manager."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        """Exit context manager."""
        await self.close()

    async def initialize(self) -> None:
        # Connect ACI and HC clients
        await asyncio.gather(
            self._aci_client.initialize(),
            self._hc_client.initialize(),
        )

        # TODO: Concurrency? Lazy loading?
        await self.areas.initialize()
        await self.loads.initialize()
        await self.stations.initialize()
        await self.buttons.initialize()
        await self.dry_contacts.initialize()
        await self.omni_sensors.initialize()
        await self.tasks.initialize()

    async def close(self) -> None:
        await asyncio.gather(
            self._aci_client.close(),
            self._hc_client.close(),
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