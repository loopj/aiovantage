"""Controllers for managing collections of objects from the Vantage system.

Controllers are responsible for fetching objects, fetching their state, and
keeping the state up to date.

Some controllers manage a single type of object, while others handle multiple types.
In controllers where multiple object types are managed, they are typically conceptually
related through shared behavior rather than a strict class hierarchy. These types of
controllers typically hold objects which implement one or more common interfaces. For
examples, objects in the [BlindsController][aiovantage.controllers.BlindsController]
all implement the [BlindInterface][aiovantage.object_interfaces.BlindInterface].

Since filtering and finding specific objects in a controller is a common operation, all
controllers all inherit from [QuerySet][aiovantage.controllers.QuerySet], which
provides a number of methods for filtering and finding objects.

An instance of every controller type is made available through the main [Vantage]
object.
"""

from ._controllers.anemo_sensors import AnemoSensorsController
from ._controllers.areas import AreasController
from ._controllers.back_box import BackBoxesController
from ._controllers.base import BaseController, VantageEvent
from ._controllers.blind_groups import BlindGroupsController
from ._controllers.blinds import BlindsController, BlindTypes
from ._controllers.buttons import ButtonsController
from ._controllers.dry_contacts import DryContactsController
from ._controllers.gmem import GMemController
from ._controllers.light_sensors import LightSensorsController
from ._controllers.load_groups import LoadGroupsController
from ._controllers.loads import LoadsController
from ._controllers.masters import MastersController
from ._controllers.modules import ModulesController
from ._controllers.omni_sensors import OmniSensorsController
from ._controllers.port_devices import PortDevicesController
from ._controllers.power_profiles import PowerProfilesController
from ._controllers.query import QuerySet
from ._controllers.rgb_loads import RGBLoadsController, RGBLoadTypes
from ._controllers.stations import StationsController
from ._controllers.tasks import TasksController
from ._controllers.temperature_sensors import TemperatureSensorsController
from ._controllers.thermostats import ThermostatsController

__all__ = [
    "AnemoSensorsController",
    "AreasController",
    "BackBoxesController",
    "BaseController",
    "BlindGroupsController",
    "BlindsController",
    "BlindTypes",
    "ButtonsController",
    "DryContactsController",
    "GMemController",
    "LightSensorsController",
    "LoadGroupsController",
    "LoadsController",
    "MastersController",
    "ModulesController",
    "OmniSensorsController",
    "PortDevicesController",
    "PowerProfilesController",
    "QuerySet",
    "RGBLoadsController",
    "RGBLoadTypes",
    "StationsController",
    "TasksController",
    "TemperatureSensorsController",
    "ThermostatsController",
    "VantageEvent",
]
