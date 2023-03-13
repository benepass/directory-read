from dataclasses import dataclass
from enum import Enum
from uuid import UUID

import pytest

from chalicelib.utils.buffer import bufferize
from chalicelib.utils.encoders import dataclass_to_dict
from chalicelib.utils.iterables import find


def test_dataclass_to_dict():
    class AEnum(str, Enum):
        b = "b"

    @dataclass
    class A:
        b: UUID
        c: tuple
        d: str
        e: AEnum

    assert dataclass_to_dict(
        A(b=UUID("4d2411f9-4dfd-4428-afb3-4911682a8ea3"), c=(1, 2, 3), d="s", e=AEnum.b)
    ) == {
        "b": "4d2411f9-4dfd-4428-afb3-4911682a8ea3",
        "c": (1, 2, 3),
        "d": "s",
        "e": "b",
    }


test_params = {
    "found": (["abc", "dfe"], "abc"),
    "not_found": (["dfe", "ghj"], None),
}


@pytest.mark.parametrize(
    "iterable, expected", test_params.values(), ids=test_params.keys()
)
def test_find_iterables(iterable, expected):
    assert find(iterable, fn=lambda k: "ab" in k) == expected


def test_bufferize_returns_consumable_buffer():
    rows = [
        {"name": "Frodo", "last_name": "Baggins", "age": "51"},
        {"name": "Bilbo", "last_name": "Baggins", "age": "129"},
    ]

    with bufferize(rows=rows) as buffer:
        assert (
            buffer.read()
            == b'[{"name": "Frodo", "last_name": "Baggins", "age": "51"}, {"name": "Bilbo", "last_name": "Baggins", "age": "129"}]'  # noqa: E501
        )
