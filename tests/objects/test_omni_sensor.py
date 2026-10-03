"""Tests for OmniSensor state fetching."""

from decimal import Decimal

from aiovantage.errors import NotInitializedError
from aiovantage.objects import OmniSensor, Parent
from tests.fakes import FakeCommandClient


def make_sensor(replies: dict[str, list[str] | Exception]) -> OmniSensor:
    """Build a temperature OmniSensor wired to a fake command client."""
    sensor = OmniSensor(
        vid=1,
        master=1,
        name="Outside",
        model="Temperature",
        note="",
        parent=Parent(vid=2, position=1),
        get=OmniSensor.Get(
            formula=OmniSensor.Get.Formula(formula="x"),
            method="Temperature.GetValue",
            method_hw="Temperature.GetValueHW",
        ),
        set=OmniSensor.Set(
            formula=OmniSensor.Set.Formula(formula="x"),
            method="Temperature.SetValue",
            method_sw="Temperature.SetValueSW",
        ),
    )
    sensor.command_client = FakeCommandClient(replies)  # type: ignore[assignment]
    return sensor


async def test_fetch_state_updates_level() -> None:
    sensor = make_sensor(
        {
            "INVOKE 1 Temperature.GetValueHW": [
                "R:INVOKE 1 21.500 Temperature.GetValueHW"
            ]
        }
    )

    assert await sensor.fetch_state() == ["level"]
    assert sensor.level == Decimal("21.5")


async def test_fetch_state_skips_level_when_not_initialized() -> None:
    sensor = make_sensor(
        {"INVOKE 1 Temperature.GetValueHW": NotInitializedError("Not Initialized")}
    )

    assert await sensor.fetch_state() == []
    assert sensor.level is None
