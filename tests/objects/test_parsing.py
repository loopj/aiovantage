"""Tests for parsing controller XML into object model dataclasses."""

import datetime as dt
from decimal import Decimal
from typing import TypeVar

from aiovantage.config_client import ConfigClient
from aiovantage.objects import (
    DryContact,
    Load,
    Parent,
    VantageDmxDaliGateway,
    VantageVirtualThermostatPort,
)

T = TypeVar("T")

# The parser is configured by the client, so borrow it rather than rebuild it
_client = ConfigClient("fake")


def parse(xml: str, cls: type[T]) -> T:
    """Parse an XML snippet into an instance of the given model class."""
    return _client._parser.from_string(xml, cls)  # type: ignore[reportPrivateUsage]


LOAD_XML = """
<Load VID="123" Master="1" MTime="2024-01-02T03:04:05.678">
  <Name>Kitchen Lights</Name>
  <Model>DIM</Model>
  <Note></Note>
  <DName>Kitchen</DName>
  <Area>45</Area>
  <Location>Kitchen</Location>
  <Parent Position="2">456</Parent>
  <ContractorNumber>K1</ContractorNumber>
  <LoadType>Incandescent</LoadType>
  <Power>60</Power>
  <PowerProfile>789</PowerProfile>
  <OverrideLevel>80.000</OverrideLevel>
</Load>
"""


def test_load_parses_every_field() -> None:
    assert parse(LOAD_XML, Load) == Load(
        vid=123,
        master=1,
        m_time=dt.datetime(2024, 1, 2, 3, 4, 5, tzinfo=dt.timezone.utc),
        name="Kitchen Lights",
        model="DIM",
        note="",
        d_name="Kitchen",
        area=45,
        location="Kitchen",
        parent=Parent(vid=456, position=2),
        contractor_number="K1",
        load_type="Incandescent",
        power=60,
        power_profile=789,
        override_level=Decimal("80"),
    )


def test_load_defaults_missing_optional_elements() -> None:
    xml = """
    <Load VID="123" Master="1">
      <Name>Hall</Name>
      <Model></Model>
      <Note></Note>
      <Area>45</Area>
      <Location>Hall</Location>
      <Parent Position="1">456</Parent>
      <ContractorNumber></ContractorNumber>
      <PowerProfile>789</PowerProfile>
    </Load>
    """

    load = parse(xml, Load)

    assert load.load_type == "Incandescent"
    assert load.power == 100
    assert load.override_level == Decimal("100")
    assert load.d_name == ""
    assert load.m_time is None


def test_unknown_elements_are_ignored() -> None:
    xml = LOAD_XML.replace("</Load>", "  <Future>1</Future>\n</Load>")

    assert parse(xml, Load).name == "Kitchen Lights"


def test_mixed_case_bool_parses() -> None:
    xml = """
    <DryContact VID="321" Master="1">
      <Name>Door</Name>
      <Model></Model>
      <Note></Note>
      <Area>45</Area>
      <Location>Hall</Location>
      <Parent Position="1">456</Parent>
      <ReversePolarity>True</ReversePolarity>
    </DryContact>
    """

    assert parse(xml, DryContact).reverse_polarity is True


def test_dmx_dali_gateway_parses_without_mode() -> None:
    # Some controllers omit the Mode element for this station, see #383
    xml = """
    <Vantage.DmxDaliGateway VID="654" Master="1">
      <Name>DMX Gateway</Name>
      <Model>DmxDaliGateway</Model>
      <Note></Note>
      <Area>45</Area>
      <Location>Cinema</Location>
      <SerialNumber>12345</SerialNumber>
      <Bus>1</Bus>
      <IPAddress>192.168.1.50</IPAddress>
    </Vantage.DmxDaliGateway>
    """

    gateway = parse(xml, VantageDmxDaliGateway)

    assert gateway.ip_address == "192.168.1.50"
    assert gateway.mode is None


def test_virtual_thermostat_parses_heating_only() -> None:
    # Heating-only thermostats have no COOL or FAN element, see #414
    xml = """
    <Vantage.VirtualThermostat_PORT VID="987" Master="1">
      <Name>Bathroom</Name>
      <Model></Model>
      <Note></Note>
      <Area>45</Area>
      <Location>Bathroom</Location>
      <changeOverValve>0</changeOverValve>
      <FrostMailFrom></FrostMailFrom>
      <FrostMailTo></FrostMailTo>
      <HEAT>
        <heatStage1Load>100</heatStage1Load>
        <heatStage1Task>0</heatStage1Task>
        <heatStage2Load>0</heatStage2Load>
        <heatStage2Task>0</heatStage2Task>
      </HEAT>
      <indoorSensorHolder>
        <indoorSensor>200</indoorSensor>
        <indoorTempOffset>0</indoorTempOffset>
      </indoorSensorHolder>
      <outdoorSensorHolder>
        <outdoorSensor>0</outdoorSensor>
        <outdoorTempOffset>0</outdoorTempOffset>
      </outdoorSensorHolder>
    </Vantage.VirtualThermostat_PORT>
    """

    thermostat = parse(xml, VantageVirtualThermostatPort)

    assert thermostat.heat is not None
    assert thermostat.heat.heat_stage_1_load == 100
    assert thermostat.cool is None
    assert thermostat.fan is None
