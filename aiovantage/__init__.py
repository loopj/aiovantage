import asyncio
from types import TracebackType
from typing import Optional, Type

from .clients.aci.client import ACIClient
from .clients.hc import HCClient
from .controllers.areas import AreasController
from .controllers.buttons import ButtonsController
from .controllers.dry_contacts import DryContactsController
from .controllers.loads import LoadsController
from .controllers.omni_sensors import OmniSensorsController
from .controllers.stations import StationsController
from .controllers.tasks import TasksController


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
        self._aci_client = ACIClient(host, username, password, use_ssl, aci_port)
        self._hc_client = HCClient(host, username, password, use_ssl, hc_port)

        self._areas = AreasController(self)
        self._loads = LoadsController(self)
        self._buttons = ButtonsController(self)
        self._dry_contacts = DryContactsController(self)
        self._omni_sensors = OmniSensorsController(self)
        self._tasks = TasksController(self)
        self._stations = StationsController(self)

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
    def omni_sensors(self) -> OmniSensorsController:
        """Return the OmniSensors controller for managing generic sensors."""
        return self._omni_sensors

    @property
    def tasks(self) -> TasksController:
        """Return the Tasks controller for managing tasks."""
        return self._tasks

    async def __aenter__(self) -> "Vantage":
        """Return Context manager."""
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] ,
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Close context manager."""
        await self.close()

    async def connect(self) -> None:
        """Initialize the clients."""
        await asyncio.gather(
            self._aci_client.connect(),
            self._hc_client.initialize(),
        )

    async def fetch_objects(self) -> None:
        """Fetch all objects from the controllers."""

        coros = [
            self._areas.fetch_objects(),
            self._loads.fetch_objects(),
            self._stations.fetch_objects(),
            self._buttons.fetch_objects(),
            self._dry_contacts.fetch_objects(),
            self._omni_sensors.fetch_objects(),
            self._tasks.fetch_objects(),
        ]

        # TODO: Connection pool? asyncio.gather?
        for coro in coros:
            await coro

    async def fetch_state(self) -> None:
        """Fetch the state of all objects."""
        await asyncio.gather(
            self._loads.fetch_state(),
            # TODO: The rest
        )

    async def close(self) -> None:
        """Close the clients."""
        await asyncio.gather(
            self._aci_client.close(),
            self._hc_client.close(),
        )
