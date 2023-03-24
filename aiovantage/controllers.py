import logging

from typing import Generic, Iterator, Type, TypeVar

from .models import Load, Area, DryContact, OmniSensor, Button, Task, Station, Variable

ItemType = TypeVar("ItemType")

class BaseController(Generic[ItemType]):
    item_type: ItemType
    event_types = None

    def __init__(self, vantage):
        self._vantage = vantage
        self._initialized = False
        self._items = {}
        self._subscribers = []
        self._logger = logging.getLogger(__name__)

    def __getitem__(self, id: str) -> ItemType:
        """Get item by id."""
        return self._items[id]

    def __iter__(self) -> Iterator[ItemType]:
        """Iterate items."""
        return iter(self._items.values())

    def __contains__(self, id: str) -> bool:
        """Return bool if id is in items."""
        return id in self._items

    async def initialize(self) -> None:
        # Fetch initial object details
        objects = await self._vantage._aci_client.fetch_objects(self.vantage_types)
        for el in objects:
            obj = self.item_type.from_xml(el)
            obj._vantage = self._vantage
            self._items[obj.id] = obj

        # Subscribe to object updates
        if self.event_types is not None:
            await self._vantage._hc_client.subscribe(self._handle_event, *self.event_types)

        self._logger.info(f"Initialized {self.__class__.__name__}")

        self._initialized = True

    def _handle_event(self, type: str, vid: int, args):
        if vid in self:
            self.handle_event(self[vid], args)
        
        for callback in self._subscribers:
            callback(self[vid], args)

    def subscribe(self, callback):
        self._subscribers.append(callback)

    def get(self, id: int, default = None):
        """Get item by id of default if item does not exist."""
        return self._items.get(id, default)

class AreasController(BaseController[Type[Area]]):
    item_type = Area
    vantage_types = ["Area"]

class LoadsController(BaseController[Type[Load]]):
    item_type = Load
    vantage_types = ["Load"]
    event_types = ["LOAD"]

    # S:LOAD {vid} {level}
    def handle_event(self, obj: Load, args):
        level = float(args[0])
        obj.level = level

        self._logger.debug(f"Load level changed for {obj.name} ({obj.id}) to {level}")

class DryContactsController(BaseController[Type[DryContact]]):
    item_type = DryContact
    vantage_types = ["DryContact"]
    event_types = ["BTN"]

    # S:BTN {vid} {PRESS|RELEASE}
    def handle_event(self, obj: DryContact, args):
        state = args[0]

        self._logger.debug(f"DryContact state changed for {obj.name} ({obj.id}) to {state}")

class ButtonsController(BaseController[Type[Button]]):
    item_type = Button
    vantage_types = ["Button"]
    event_types = ["BTN"]

    # S:BTN {vid} {PRESS|RELEASE}
    def handle_event(self, obj: Button, args):
        state = args[0]

        self._logger.debug(f"Button state changed for {obj.name} {obj.text} ({obj.id}) to {state}")

class OmniSensorsController(BaseController[Type[OmniSensor]]):
    item_type = OmniSensor
    vantage_types = ["OmniSensor"]
    event_types = ["TEMP", "POWER", "CURRENT"]

    # S:TEMP {vid} {level}
    # S:POWER {vid} {level}
    # S:CURRENT {vid} {level}
    def handle_event(self, obj: OmniSensor, args):
        level = float(args[0])
        obj.level = level

        self._logger.debug(f"OmniSensor level changed for {obj.name} ({obj.id}) to {level}")

class TasksController(BaseController[Type[Task]]):
    item_type = Task
    vantage_types = ["Task"]
    event_types = ["TASK"]

    # S:TASK {vid} {state}
    def handle_event(self, obj: Task, args):
        state = int(args[0])
        self._logger.debug(f"Task triggered {obj.name} ({obj.id}) to {state}")

class StationsController(BaseController[Type[Station]]):
    item_type = Station
    vantage_types = ["Keypad", "Dimmer", "ScenePointRelay", "DualRelayStation", "EqCtrl", "EqUX"]

class VariablesController(BaseController[Type[Variable]]):
    item_type = Variable
    vantage_types = ["GMem"]
    event_types = ["VARIABLE"]