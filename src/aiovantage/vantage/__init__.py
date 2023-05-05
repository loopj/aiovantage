import asyncio
from types import TracebackType
from typing import Callable, Optional, Type

from aiovantage.command_client import CommandClient
from aiovantage.config_client import ConfigClient
from aiovantage.config_client.objects import SystemObject
from aiovantage.vantage.controllers.areas import AreasController
from aiovantage.vantage.controllers.base import EventCallback
from aiovantage.vantage.controllers.buttons import ButtonsController
from aiovantage.vantage.controllers.dry_contacts import DryContactsController
from aiovantage.vantage.controllers.gmem import GMemController
from aiovantage.vantage.controllers.loads import LoadsController
from aiovantage.vantage.controllers.rgb_loads import RGBLoadsController
from aiovantage.vantage.controllers.sensors import SensorsController
from aiovantage.vantage.controllers.stations import StationsController
from aiovantage.vantage.controllers.tasks import TasksController


class Vantage:
    """Control a Vantage InFusion controller."""

    def __init__(
        self,
        host: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        *,
        use_ssl: bool = True,
        config_port: Optional[int] = None,
        command_port: Optional[int] = None,
    ) -> None:
        """Initialize the Vantage instance."""

        # Set up config and command clients
        self._config_client = ConfigClient(
            host, username, password, use_ssl=use_ssl, port=config_port
        )

        self._command_client = CommandClient(
            host, username, password, use_ssl=use_ssl, port=command_port
        )

        # Set up controllers
        self._areas = AreasController(self)
        self._buttons = ButtonsController(self)
        self._dry_contacts = DryContactsController(self)
        self._gmem = GMemController(self)
        self._loads = LoadsController(self)
        self._rgb_loads = RGBLoadsController(self)
        self._sensors = SensorsController(self)
        self._stations = StationsController(self)
        self._tasks = TasksController(self)

    async def __aenter__(self) -> "Vantage":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.close()

    @property
    def config_client(self) -> ConfigClient:
        """Return the config client."""
        return self._config_client

    @property
    def command_client(self) -> CommandClient:
        """Return the command client."""
        return self._command_client

    @property
    def areas(self) -> AreasController:
        """Return the Areas controller for managing areas."""
        return self._areas

    @property
    def buttons(self) -> ButtonsController:
        """Return the Buttons controller for managing buttons."""
        return self._buttons

    @property
    def dry_contacts(self) -> DryContactsController:
        """Return the DryContacts controller for managing dry contacts."""
        return self._dry_contacts

    @property
    def loads(self) -> LoadsController:
        """Return the Loads controller for managing loads (lights, fans, etc)."""
        return self._loads

    @property
    def gmem(self) -> GMemController:
        """Return the GMem controller for managing global memory."""
        return self._gmem

    @property
    def rgb_loads(self) -> RGBLoadsController:
        """Return the RGBLoads controller for managing RGB loads."""
        return self._rgb_loads

    @property
    def sensors(self) -> SensorsController:
        """Return the OmniSensors controller for managing generic sensors."""
        return self._sensors

    @property
    def stations(self) -> StationsController:
        """Return the Stations controller for managing stations (keypads, etc)."""
        return self._stations

    @property
    def tasks(self) -> TasksController:
        """Return the Tasks controller for managing tasks."""
        return self._tasks

    def close(self) -> None:
        """Close the clients."""

        self.config_client.close()
        self.command_client.close()

    async def initialize(self) -> None:
        """Fetch all objects from the controllers."""

        await asyncio.gather(
            self._areas.initialize(),
            self._buttons.initialize(),
            self._dry_contacts.initialize(),
            self._gmem.initialize(),
            self._loads.initialize(),
            self._rgb_loads.initialize(),
            self._sensors.initialize(),
            self._stations.initialize(),
            self._tasks.initialize(),
        )

    def subscribe(self, callback: EventCallback[SystemObject]) -> Callable[[], None]:
        """
        Subscribe to state changes for all objects.

        Returns:
            A function to unsubscribe.
        """

        unsubscribes = [
            self.buttons.subscribe(callback),
            self.dry_contacts.subscribe(callback),
            self.gmem.subscribe(callback),
            self.loads.subscribe(callback),
            self.rgb_loads.subscribe(callback),
            self.sensors.subscribe(callback),
            self.tasks.subscribe(callback),
        ]

        def unsubscribe() -> None:
            for unsub in unsubscribes:
                unsub()

        return unsubscribe
