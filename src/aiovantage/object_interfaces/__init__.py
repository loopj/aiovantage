"""Object interfaces classes."""

from .anemo_sensor import AnemoSensorInterface
from .blind import BlindInterface
from .button import ButtonInterface
from .color_temperature import ColorTemperatureInterface
from .configuration import ConfigurationInterface
from .current_sensor import CurrentSensorInterface
from .fan import FanInterface
from .gmem import GMemInterface
from .introspection import IntrospectionInterface
from .light_sensor import LightSensorInterface
from .load import LoadInterface
from .object import ObjectInterface
from .power_sensor import PowerSensorInterface
from .rgb_load import RGBLoadInterface
from .sensor import SensorInterface
from .sounder import SounderInterface
from .task import TaskInterface
from .temperature import TemperatureInterface
from .thermostat import ThermostatInterface

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
