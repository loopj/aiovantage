"""Interact with and control Vantage InFusion home automation controllers."""

__all__ = ["Vantage", "VantageEvent"]

import asyncio
from types import TracebackType
from typing import Callable, Optional, Type

from typing_extensions import Self

from aiovantage.command_client import CommandClient, EventStream
from aiovantage.config_client import ConfigClient
from aiovantage.config_client.objects import SystemObject
from aiovantage.controllers.anemo_sensors import AnemoSensorsController
from aiovantage.controllers.areas import AreasController
from aiovantage.controllers.base import EventCallback
from aiovantage.controllers.blind_groups import BlindGroupsController
from aiovantage.controllers.blinds import BlindsController
from aiovantage.controllers.buttons import ButtonsController
from aiovantage.controllers.dry_contacts import DryContactsController
from aiovantage.controllers.gmem import GMemController
from aiovantage.controllers.light_sensors import LightSensorsController
from aiovantage.controllers.load_groups import LoadGroupsController
from aiovantage.controllers.loads import LoadsController
from aiovantage.controllers.masters import MastersController
from aiovantage.controllers.omni_sensors import OmniSensorsController
from aiovantage.controllers.rgb_loads import RGBLoadsController
from aiovantage.controllers.stations import StationsController
from aiovantage.controllers.tasks import TasksController
from aiovantage.controllers.temperature_sensors import TemperatureSensorsController

from .events import VantageEvent


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

        # Set up clients
        self._config_client = ConfigClient(
            host, username, password, ssl=use_ssl, port=config_port
        )

        self._command_client = CommandClient(
            host, username, password, ssl=use_ssl, port=command_port
        )

        self._event_stream = EventStream(
            host, username, password, ssl=use_ssl, port=command_port
        )

        # Set up controllers
        self._anemo_sensors = AnemoSensorsController(self)
        self._areas = AreasController(self)
        self._blinds = BlindsController(self)
        self._blind_groups = BlindGroupsController(self)
        self._buttons = ButtonsController(self)
        self._dry_contacts = DryContactsController(self)
        self._gmem = GMemController(self)
        self._light_sensors = LightSensorsController(self)
        self._loads = LoadsController(self)
        self._load_groups = LoadGroupsController(self)
        self._masters = MastersController(self)
        self._rgb_loads = RGBLoadsController(self)
        self._omni_sensors = OmniSensorsController(self)
        self._stations = StationsController(self)
        self._tasks = TasksController(self)
        self._temperature_sensors = TemperatureSensorsController(self)

    async def __aenter__(self) -> Self:
        """Return context manager."""
        await self.event_stream.start()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit context manager."""
        await self.close()
        if exc_val:
            raise exc_val

    @property
    def config_client(self) -> ConfigClient:
        """Return the config client."""
        return self._config_client

    @property
    def command_client(self) -> CommandClient:
        """Return the command client."""
        return self._command_client

    @property
    def event_stream(self) -> EventStream:
        """Return the event stream."""
        return self._event_stream

    @property
    def anemo_sensors(self) -> AnemoSensorsController:
        """Return the AnemoSensors controller for managing anemo sensors."""
        return self._anemo_sensors

    @property
    def areas(self) -> AreasController:
        """Return the Areas controller for managing areas."""
        return self._areas

    @property
    def blinds(self) -> BlindsController:
        """Return the Blinds controller for managing blinds."""
        return self._blinds

    @property
    def blind_groups(self) -> BlindGroupsController:
        """Return the BlindGroups controller for managing groups of blinds."""
        return self._blind_groups

    @property
    def buttons(self) -> ButtonsController:
        """Return the Buttons controller for managing buttons."""
        return self._buttons

    @property
    def dry_contacts(self) -> DryContactsController:
        """Return the DryContacts controller for managing dry contacts."""
        return self._dry_contacts

    @property
    def light_sensors(self) -> LightSensorsController:
        """Return the LightSensors controller for managing light sensors."""
        return self._light_sensors

    @property
    def loads(self) -> LoadsController:
        """Return the Load controller for managing loads (lights, fans, etc)."""
        return self._loads

    @property
    def load_groups(self) -> LoadGroupsController:
        """Return the LoadGroup controller for managing groups of loads."""
        return self._load_groups

    @property
    def masters(self) -> MastersController:
        """Return the Masters controller for managing Vantage Controllers."""
        return self._masters

    @property
    def gmem(self) -> GMemController:
        """Return the GMem controller for managing global memory."""
        return self._gmem

    @property
    def omni_sensors(self) -> OmniSensorsController:
        """Return the OmniSensors controller for managing generic sensors."""
        return self._omni_sensors

    @property
    def rgb_loads(self) -> RGBLoadsController:
        """Return the RGBLoads controller for managing RGB loads."""
        return self._rgb_loads

    @property
    def stations(self) -> StationsController:
        """Return the Stations controller for managing stations (keypads, etc)."""
        return self._stations

    @property
    def tasks(self) -> TasksController:
        """Return the Tasks controller for managing tasks."""
        return self._tasks

    @property
    def temperature_sensors(self) -> TemperatureSensorsController:
        """Return the TemperatureSensors controller for managing temperature sensors."""
        return self._temperature_sensors

    async def close(self) -> None:
        """Close the clients."""

        self.config_client.close()
        self.command_client.close()
        await self.event_stream.stop()

    async def initialize(self) -> None:
        """Fetch all objects from the controllers."""

        await asyncio.gather(
            self._anemo_sensors.initialize(),
            self._areas.initialize(),
            self._blinds.initialize(),
            self._blind_groups.initialize(),
            self._buttons.initialize(),
            self._dry_contacts.initialize(),
            self._gmem.initialize(),
            self._light_sensors.initialize(),
            self._loads.initialize(),
            self._masters.initialize(),
            self._rgb_loads.initialize(),
            self._omni_sensors.initialize(),
            self._stations.initialize(),
            self._tasks.initialize(),
            self._temperature_sensors.initialize(),
        )

    def subscribe(self, callback: EventCallback[SystemObject]) -> Callable[[], None]:
        """Subscribe to state changes for all objects.

        Returns:
            A function to unsubscribe.
        """

        unsubscribes = [
            self.anemo_sensors.subscribe(callback),
            self.areas.subscribe(callback),
            self.blinds.subscribe(callback),
            self.blind_groups.subscribe(callback),
            self.buttons.subscribe(callback),
            self.dry_contacts.subscribe(callback),
            self.gmem.subscribe(callback),
            self.light_sensors.subscribe(callback),
            self.loads.subscribe(callback),
            self.masters.subscribe(callback),
            self.rgb_loads.subscribe(callback),
            self.omni_sensors.subscribe(callback),
            self.stations.subscribe(callback),
            self.tasks.subscribe(callback),
            self.temperature_sensors.subscribe(callback),
        ]

        def unsubscribe() -> None:
            for unsub in unsubscribes:
                unsub()

        return unsubscribe
