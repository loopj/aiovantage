"""Interact with and control Vantage InFusion home automation controllers."""

__all__ = ["Vantage", "VantageEvent"]

import asyncio
from types import TracebackType
from typing import Any, Callable, Optional, Set, Type, TypeVar

from typing_extensions import Self

from .command_client import CommandClient, Event, EventStream, EventType
from .config_client import ConfigClient
from .controllers import (
    AnemoSensorsController,
    AreasController,
    BaseController,
    BlindGroupsController,
    BlindsController,
    ButtonsController,
    DryContactsController,
    GMemController,
    LightSensorsController,
    LoadGroupsController,
    LoadsController,
    MastersController,
    ModulesController,
    OmniSensorsController,
    PortDevicesController,
    RGBLoadsController,
    StationsController,
    TasksController,
    TemperatureSensorsController,
)
from .events import EventCallback, VantageEvent
from .models import SystemObject

ControllerT = TypeVar("ControllerT", bound=BaseController[Any])


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
        """Initialize the Vantage instance.

        Args:
            host: The hostname or IP address of the Vantage controller.
            username: The username to use for authentication.
            password: The password to use for authentication.
            use_ssl: Whether to use SSL for the connection.
            config_port: The port to use for the config client.
            command_port: The port to use for the command client.
        """
        # Set up clients
        self._host = host
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
        self._controllers: Set[BaseController[Any]] = set()
        self._anemo_sensors = self._add_controller(AnemoSensorsController)
        self._areas = self._add_controller(AreasController)
        self._blind_groups = self._add_controller(BlindGroupsController)
        self._blinds = self._add_controller(BlindsController)
        self._buttons = self._add_controller(ButtonsController)
        self._dry_contacts = self._add_controller(DryContactsController)
        self._gmem = self._add_controller(GMemController)
        self._light_sensors = self._add_controller(LightSensorsController)
        self._load_groups = self._add_controller(LoadGroupsController)
        self._loads = self._add_controller(LoadsController)
        self._masters = self._add_controller(MastersController)
        self._modules = self._add_controller(ModulesController)
        self._rgb_loads = self._add_controller(RGBLoadsController)
        self._omni_sensors = self._add_controller(OmniSensorsController)
        self._port_devices = self._add_controller(PortDevicesController)
        self._stations = self._add_controller(StationsController)
        self._tasks = self._add_controller(TasksController)
        self._temperature_sensors = self._add_controller(TemperatureSensorsController)

    async def __aenter__(self) -> Self:
        """Return context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit context manager."""
        self.close()
        if exc_val:
            raise exc_val

    @property
    def host(self) -> str:
        """Return the hostname or IP address of the Vantage controller."""
        return self._host

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
    def gmem(self) -> GMemController:
        """Return the GMem controller for managing variables."""
        return self._gmem

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
    def modules(self) -> ModulesController:
        """Return the Modules controller for managing dimmer modules."""
        return self._modules

    @property
    def omni_sensors(self) -> OmniSensorsController:
        """Return the OmniSensors controller for managing omni sensors."""
        return self._omni_sensors

    @property
    def port_devices(self) -> PortDevicesController:
        """Return the PortDevices controller for managing port devices."""
        return self._port_devices

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

    @property
    def known_ids(self) -> Set[int]:
        """Return a set of all known object IDs."""
        return {vid for controller in self._controllers for vid in controller.known_ids}

    def close(self) -> None:
        """Close the clients."""
        self.config_client.close()
        self.command_client.close()
        self.event_stream.stop()

    async def initialize(self, fetch_state: bool = True) -> None:
        """Fetch all objects from the controllers.

        Args:
            fetch_state: Whether to also fetch the state of each object.
        """
        # Initialize all controllers
        await asyncio.gather(
            *[controller.initialize(fetch_state) for controller in self._controllers]
        )

        # Start the event stream
        await self.event_stream.start()

        # Subscribe to reconnect events
        self.event_stream.subscribe(self._handle_event, EventType.RECONNECTED)

    def subscribe(self, callback: EventCallback[SystemObject]) -> Callable[[], None]:
        """Subscribe to state changes for all objects.

        Args:
            callback: The callback to call when an object changes.

        Returns:
            A function to unsubscribe.
        """
        unsubscribes = [
            controller.subscribe(callback) for controller in self._controllers
        ]

        def unsubscribe() -> None:
            for unsub in unsubscribes:
                unsub()

        return unsubscribe

    async def _handle_event(self, event: Event) -> None:
        # Handle events from the event stream.
        if event["type"] == EventType.RECONNECTED:
            for controller in self._controllers:
                if controller.initialized:
                    await controller.fetch_full_state()

    def _add_controller(self, controller_cls: Type[ControllerT]) -> ControllerT:
        # Add a controller to the known controllers.
        controller = controller_cls(self)
        self._controllers.add(controller)
        return controller
