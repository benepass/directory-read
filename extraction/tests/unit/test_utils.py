from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from chalicelib.utils.encoders import dataclass_to_dict


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
