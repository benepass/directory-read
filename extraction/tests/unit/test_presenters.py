from chalicelib.presenters.custom import CustomPresenter


def test_custom_presenter_to_dict():
    reason = "Something really wrong happened"
    assert CustomPresenter(ok=False, reason=reason).to_dict() == {
        "ok": False,
        "reason": reason,
    }
