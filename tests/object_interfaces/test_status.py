"""Tests for applying status messages to object interface properties."""

from decimal import Decimal
from typing import Any

import pytest

from aiovantage.object_interfaces import (
    BlindInterface,
    ButtonInterface,
    GMemInterface,
    Interface,
    LoadInterface,
    TaskInterface,
)


def test_object_status_updates_mapped_property() -> None:
    load = LoadInterface()

    assert load.handle_object_status("Load.GetLevel", "75000") == ["level"]
    assert load.level == Decimal("75")


def test_object_status_ignores_unmapped_method() -> None:
    load = LoadInterface()

    assert load.handle_object_status("Load.GetProfile", "3") == []
    assert load.level is None


def test_object_status_reports_nothing_when_unchanged() -> None:
    load = LoadInterface()
    load.level = Decimal("75")

    assert load.handle_object_status("Load.GetLevel", "75000") == []


def test_object_status_builds_dataclass_property() -> None:
    blind = BlindInterface()

    changed = blind.handle_object_status(
        "Blind.GetBlindState", "1", "0.000", "100.000", "2.500", "12345"
    )

    assert changed == ["blind_state"]
    assert blind.blind_state == BlindInterface.BlindState(
        is_moving=True,
        start_pos=Decimal("0"),
        end_pos=Decimal("100"),
        transition_time=Decimal("2.5"),
        start_time=12345,
    )


@pytest.mark.parametrize(
    ("cls", "category", "arg", "prop", "expected"),
    [
        pytest.param(LoadInterface, "LOAD", "75", "level", Decimal("75"), id="load"),
        pytest.param(TaskInterface, "TASK", "1", "state", 1, id="task"),
        pytest.param(
            ButtonInterface,
            "BTN",
            "PRESS",
            "state",
            ButtonInterface.State.Down,
            id="button",
        ),
        pytest.param(GMemInterface, "VARIABLE", "3", "value", 3, id="gmem-int"),
        pytest.param(GMemInterface, "VARIABLE", '"on"', "value", "on", id="gmem-str"),
    ],
)
def test_category_status_updates_property(
    cls: type[Interface], category: str, arg: str, prop: str, expected: Any
) -> None:
    obj = cls()

    assert obj.handle_category_status(category, arg) == [prop]
    assert getattr(obj, prop) == expected


def test_category_status_ignores_foreign_category() -> None:
    load = LoadInterface()

    assert load.handle_category_status("TASK", "1") == []
    assert load.level is None
