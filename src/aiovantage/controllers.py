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

from aiovantage._controllers.anemo_sensors import AnemoSensorsController
from aiovantage._controllers.areas import AreasController
from aiovantage._controllers.back_box import BackBoxesController
from aiovantage._controllers.base import BaseController
from aiovantage._controllers.blind_groups import BlindGroupsController
from aiovantage._controllers.blinds import BlindsController, BlindTypes
from aiovantage._controllers.buttons import ButtonsController
from aiovantage._controllers.dry_contacts import DryContactsController
from aiovantage._controllers.gmem import GMemController
from aiovantage._controllers.light_sensors import LightSensorsController
from aiovantage._controllers.load_groups import LoadGroupsController
from aiovantage._controllers.loads import LoadsController
from aiovantage._controllers.masters import MastersController
from aiovantage._controllers.modules import ModulesController
from aiovantage._controllers.omni_sensors import OmniSensorsController
from aiovantage._controllers.port_devices import PortDevicesController
from aiovantage._controllers.power_profiles import PowerProfilesController
from aiovantage._controllers.query import QuerySet
from aiovantage._controllers.rgb_loads import RGBLoadsController, RGBLoadTypes
from aiovantage._controllers.stations import StationsController
from aiovantage._controllers.tasks import TasksController
from aiovantage._controllers.temperature_sensors import TemperatureSensorsController
from aiovantage._controllers.thermostats import ThermostatsController

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
]
