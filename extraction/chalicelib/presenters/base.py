from dataclasses import dataclass

from chalicelib.utils.encoders import dataclass_to_dict


@dataclass(frozen=True)
class PresenterToDictMixin:
    def to_dict(self) -> dict:
        return dataclass_to_dict(self)
