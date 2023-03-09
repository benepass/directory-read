from dataclasses import asdict
from uuid import UUID

from chalicelib.adapters.types import DataClass


def dataclass_to_dict(obj: DataClass) -> dict:
    d = asdict(obj)

    for k, v in d.items():
        if isinstance(d[k], UUID):
            d[k] = str(v)

    return d
