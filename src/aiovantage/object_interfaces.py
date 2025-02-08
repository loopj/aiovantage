"""Object interfaces classes."""

from ._object_interfaces.anemo_sensor import AnemoSensorInterface
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
