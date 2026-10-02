"""Tests for sending INVOKE requests and parsing replies in Interface.invoke()."""

from decimal import Decimal
from typing import TypeVar

import pytest

from aiovantage.errors import CommandError
from aiovantage.object_interfaces import (
    BlindInterface,
    ButtonInterface,
    Interface,
    LoadInterface,
    ObjectInterface,
    TaskInterface,
)
from tests.fakes import FakeCommandClient

T = TypeVar("T", bound=Interface)


def make(cls: type[T], vid: int, sent: str, *reply: str) -> T:
    """Build an interface of the given type wired to a fake that answers one request."""
    obj = cls()
    obj.vid = vid
    obj.command_client = FakeCommandClient({sent: list(reply)})  # type: ignore[assignment]
    return obj


async def test_invoke_parses_decimal_from_result() -> None:
    load = make(
        LoadInterface, 1, "INVOKE 1 Load.GetLevel", "R:INVOKE 1 75.000 Load.GetLevel"
    )

    assert await load.get_level() == Decimal("75")


async def test_invoke_parses_int_from_result() -> None:
    load = make(
        LoadInterface, 1, "INVOKE 1 Load.GetProfile", "R:INVOKE 1 3 Load.GetProfile"
    )

    assert await load.get_profile() == 3


async def test_invoke_parses_bool_from_result() -> None:
    task = make(
        TaskInterface, 1, "INVOKE 1 Task.IsRunning", "R:INVOKE 1 1 Task.IsRunning"
    )

    assert await task.is_running() is True


async def test_invoke_parses_enum_by_name() -> None:
    button = make(
        ButtonInterface,
        1,
        "INVOKE 1 Button.GetState",
        "R:INVOKE 1 Down Button.GetState",
    )

    assert await button.get_state() == ButtonInterface.State.Down


async def test_invoke_parses_enum_by_value() -> None:
    button = make(
        ButtonInterface, 1, "INVOKE 1 Button.GetState", "R:INVOKE 1 1 Button.GetState"
    )

    assert await button.get_state() == ButtonInterface.State.Down


async def test_invoke_parses_quoted_str_from_arg0() -> None:
    obj = make(
        ObjectInterface,
        1,
        "INVOKE 1 Object.GetName",
        'R:INVOKE 1 0 Object.GetName "Kitchen Lights"',
    )

    assert await obj.get_name() == "Kitchen Lights"


async def test_invoke_parses_dataclass_from_result_and_args() -> None:
    blind = make(
        BlindInterface,
        1,
        "INVOKE 1 Blind.GetBlindState",
        "R:INVOKE 1 0 Blind.GetBlindState 0.000 100.000 2.500 12345",
    )

    assert await blind.get_blind_state() == BlindInterface.BlindState(
        is_moving=False,
        start_pos=Decimal("0"),
        end_pos=Decimal("100"),
        transition_time=Decimal("2.5"),
        start_time=12345,
    )


async def test_invoke_returns_none_for_setter() -> None:
    load = make(
        LoadInterface,
        1,
        "INVOKE 1 Load.SetLevel 75",
        "R:INVOKE 1 0 Load.SetLevel 75.000",
    )

    assert await load.set_level(75) is None


async def test_invoke_serializes_params() -> None:
    sent = "INVOKE 1 Load.Ramp 5 2.500 100"
    load = make(LoadInterface, 1, sent, "R:INVOKE 1 0 Load.Ramp 5 2.500 100")

    await load.ramp(LoadInterface.RampType.Up, 2.5, 100)

    assert load.command_client.sent == [sent]  # type: ignore[union-attr]


async def test_invoke_quotes_str_params_and_reads_arg1() -> None:
    sent = 'INVOKE 1 Object.GetPropertyEx "Name"'
    obj = make(
        ObjectInterface,
        1,
        sent,
        'R:INVOKE 1 0 Object.GetPropertyEx "Name" "Kitchen"',
    )

    assert await obj.get_property_ex("Name") == "Kitchen"
    assert obj.command_client.sent == [sent]  # type: ignore[union-attr]


async def test_fetch_state_updates_properties() -> None:
    load = make(
        LoadInterface, 1, "INVOKE 1 Load.GetLevel", "R:INVOKE 1 75.000 Load.GetLevel"
    )

    assert await load.fetch_state() == ["level"]
    assert load.level == Decimal("75")


@pytest.mark.parametrize(
    ("reply", "expected"),
    [
        pytest.param(
            "R:INVOKE 448 100.000 Load.GetLevel", Decimal("100.000"), id="modern"
        ),
        # Older firmware answers INVOKE with the legacy GETLOAD reply, see #379
        pytest.param("R:GETLOAD 448 100.000", Decimal("100.000"), id="legacy"),
    ],
)
async def test_get_level_parses_reply(reply: str, expected: Decimal) -> None:
    load = make(LoadInterface, 448, "INVOKE 448 Load.GetLevel", reply)

    assert await load.get_level() == expected


@pytest.mark.parametrize(
    "reply",
    [
        pytest.param("R:INVOKE 141 0 Load.SetLevel 100.000", id="modern"),
        # Older firmware answers INVOKE with the legacy LOAD reply, see #313
        pytest.param("R:LOAD 141 100.000", id="legacy"),
    ],
)
async def test_set_level_accepts_reply(reply: str) -> None:
    load = make(LoadInterface, 141, "INVOKE 141 Load.SetLevel 100", reply)

    await load.set_level(100)


@pytest.mark.parametrize(
    "reply",
    [
        pytest.param("R:INVOKE 448", id="too-short"),
        pytest.param("R:GETLOAD 999 100.000", id="wrong-vid"),
        pytest.param("R:GETTASK 448 1", id="wrong-legacy-command"),
    ],
)
async def test_invoke_rejects_unexpected_reply(reply: str) -> None:
    load = make(LoadInterface, 448, "INVOKE 448 Load.GetLevel", reply)

    with pytest.raises(CommandError):
        await load.get_level()


async def test_fetch_state_skips_property_with_unexpected_reply() -> None:
    load = make(LoadInterface, 448, "INVOKE 448 Load.GetLevel", "R:INVOKE 448")

    assert await load.fetch_state() == []
    assert load.level is None
