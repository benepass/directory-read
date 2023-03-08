from typing import Any, Callable

from chalice.app import BaseLambdaEvent, Blueprint, MiddlewareHandler

from chalicelib.config import capture_monitored_exception
from chalicelib.presenters.custom import CustomPresenter

middlewares = Blueprint(__name__)


@middlewares.middleware("all")
def log_events(event: BaseLambdaEvent, get_response: MiddlewareHandler) -> Any:
    middlewares.log.info(f"event {event.to_dict()} to be handled")
    response = get_response(event)
    middlewares.log.info(f"handled {response} event")
    return response


@middlewares.middleware("all")
def handle_exception(event: BaseLambdaEvent, get_response: Callable) -> Any:
    try:
        response = get_response(event)
    except Exception as exp:
        capture_monitored_exception(exp)
        return CustomPresenter(ok=False, reason=exp.message).to_dict()
    return response
