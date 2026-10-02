"""Tests for Host Command service token conversion."""

import datetime as dt
import struct
from decimal import Decimal
from enum import IntEnum
from typing import Any

import pytest

from aiovantage.command_client import Converter
from aiovantage.errors import ConversionError

EPOCH = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)


class State(IntEnum):
    """Enum used to exercise enum conversion."""

    Up = 0
    Down = 1


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        pytest.param(
            "R:INVOKE 1 75.000 Load.GetLevel",
            ["R:INVOKE", "1", "75.000", "Load.GetLevel"],
            id="plain",
        ),
        pytest.param(
            'R:INVOKE 1 0 Object.GetName "Kitchen Lights"',
            ["R:INVOKE", "1", "0", "Object.GetName", '"Kitchen Lights"'],
            id="quoted-with-space",
        ),
        pytest.param(
            '"Say ""hi"" now"',
            ['"Say ""hi"" now"'],
            id="quoted-with-escaped-quotes",
        ),
        pytest.param("R:X {1,2,3} end", ["R:X", "{1,2,3}", "end"], id="curly-bytes"),
        pytest.param("R:X [1 2 3] end", ["R:X", "[1 2 3]", "end"], id="square-bytes"),
    ],
)
def test_tokenize(string: str, expected: list[str]) -> None:
    assert Converter.tokenize(string) == expected


@pytest.mark.parametrize(
    ("data_type", "value", "expected"),
    [
        pytest.param(str, '"Kitchen ""Lights"""', 'Kitchen "Lights"', id="str-quoted"),
        pytest.param(str, "Load", "Load", id="str-bare"),
        pytest.param(bool, "1", True, id="bool"),
        pytest.param(int, "3", 3, id="int"),
        pytest.param(float, "2.5", 2.5, id="float"),
        pytest.param(Decimal, "75.000", Decimal("75"), id="decimal-invoke-form"),
        pytest.param(Decimal, "75000", Decimal("75"), id="decimal-status-form"),
        pytest.param(bytes, "{1,2}", struct.pack("ii", 1, 2), id="bytes"),
        pytest.param(dt.datetime, "0", EPOCH, id="datetime"),
        pytest.param(State, "Down", State.Down, id="enum-by-name"),
        pytest.param(State, "1", State.Down, id="enum-by-value"),
    ],
)
def test_deserialize(data_type: type, value: str, expected: Any) -> None:
    assert Converter.deserialize(data_type, value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param('Kitchen "Lights"', '"Kitchen ""Lights"""', id="str"),
        pytest.param(True, "1", id="bool"),
        pytest.param(3, "3", id="int"),
        pytest.param(2.5, "2.500", id="float"),
        pytest.param(Decimal("75"), "75.000", id="decimal"),
        pytest.param(State.Down, "1", id="enum"),
        pytest.param(b"\x01", "{1}", id="bytes-padded"),
        pytest.param(EPOCH, "0", id="datetime"),
    ],
)
def test_serialize(value: Any, expected: str) -> None:
    assert Converter.serialize(value) == expected


@pytest.mark.parametrize(
    ("data_type", "value"),
    [
        pytest.param(int, "abc", id="bad-value"),
        pytest.param(object, "x", id="unregistered-type"),
    ],
)
def test_deserialize_raises_conversion_error(data_type: type, value: str) -> None:
    with pytest.raises(ConversionError):
        Converter.deserialize(data_type, value)
