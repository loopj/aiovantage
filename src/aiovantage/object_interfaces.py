"""Object interfaces classes.

Object interface classes define how an object's state is accessed and modified. Each
object implements one or more interfaces, with all objects automatically supporting
[`ObjectInterface`][aiovantage.object_interfaces.ObjectInterface] through inheritance
from [`SystemObject`][aiovantage.objects.SystemObject].

Object interfaces expose *state* properties, which represent dynamic attributes that
change during the operation of the system, such as the level a light or the current
temperature of a thermostat. These properties are distinct from *configuration*
properties, which are set when the system is programmed from Design Center and remain
fixed during normal operation.

State properties can be retrieved using [`fetch_state`][aiovantage.object_interfaces.Interface.fetch_state]
and are kept up to date by calling [`handle_object_status`][aiovantage.object_interfaces.Interface.handle_object_status]
or [`handle_category_status`][aiovantage.object_interfaces.Interface.handle_category_status] when messages are received from the
command client event stream.

In practice, controllers are responsible for managing state properties. They handle the
initial retrieval of state, process updates from the event stream, and ensure that the
latest state is reflected in the system.
"""

from ._object_interfaces.anemo_sensor import AnemoSensorInterface
from ._object_interfaces.base import Interface
from ._object_interfaces.blind import BlindInterface
from ._object_interfaces.button import ButtonInterface
from ._object_interfaces.color_temperature import ColorTemperatureInterface
from ._object_interfaces.configuration import ConfigurationInterface
from ._object_interfaces.current_sensor import CurrentSensorInterface
from ._object_interfaces.fan import FanInterface
from ._object_interfaces.gmem import GMemInterface
from ._object_interfaces.introspection import IntrospectionInterface
from ._object_interfaces.light_sensor import LightSensorInterface
from ._object_interfaces.load import LoadInterface
from ._object_interfaces.object import ObjectInterface
from ._object_interfaces.power_sensor import PowerSensorInterface
from ._object_interfaces.rgb_load import RGBLoadInterface
from ._object_interfaces.sensor import SensorInterface
from ._object_interfaces.sounder import SounderInterface
from ._object_interfaces.task import TaskInterface
from ._object_interfaces.temperature import TemperatureInterface
from ._object_interfaces.thermostat import ThermostatInterface

__all__ = [
    "AnemoSensorInterface",
    "BlindInterface",
    "ButtonInterface",
    "ColorTemperatureInterface",
    "ConfigurationInterface",
    "CurrentSensorInterface",
    "FanInterface",
    "GMemInterface",
    "Interface",
    "IntrospectionInterface",
    "LightSensorInterface",
    "LoadInterface",
    "ObjectInterface",
    "PowerSensorInterface",
    "RGBLoadInterface",
    "SensorInterface",
    "SounderInterface",
    "TaskInterface",
    "TemperatureInterface",
    "ThermostatInterface",
]
