from dataclasses import dataclass

from chalicelib.presenters.base import PresenterToDictMixin


@dataclass(frozen=True)
class CustomPresenter(PresenterToDictMixin):
    ok: bool

    data: str = ""
    reason: str = ""

    def to_dict(self) -> dict:
        as_dict = super().to_dict()

        if as_dict["ok"]:
            del as_dict["reason"]
        else:
            del as_dict["data"]

        return as_dict
