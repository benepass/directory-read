from functools import partial
from http import HTTPStatus
from logging import Logger
from typing import Any, Dict, Iterator

import httpx
from tenacity import RetryCallState, after, before, retry, retry_if_result, stop, wait

from chalicelib.config import MergeAPICredentials, get_maximum_request_attempts

QueryParams = Dict[str, Any]


class MergeAPIClientException(Exception):
    pass


def raise_client_api_exception(retry_call: RetryCallState):
    last_call_outcome = retry_call.outcome
    if last_call_outcome is None:
        error_msg = str(retry_call)
    elif isinstance(last_call_outcome.exception(), Exception):
        error_msg = str(last_call_outcome.exception())
    else:
        error_msg = last_call_outcome.result().text

    raise MergeAPIClientException({"reason": error_msg})


def is_req_retriable(resp: httpx.Response) -> bool:
    return resp.status_code in (
        HTTPStatus.INTERNAL_SERVER_ERROR,
        HTTPStatus.REQUEST_TIMEOUT,
        HTTPStatus.TOO_MANY_REQUESTS,
    )


def log_request(logger: Logger, request: httpx.Request):
    logger.info(
        f"Request event hook: {request.method} {request.url} - Waiting for response"
    )


def log_response(logger: Logger, response: httpx.Response):
    req = response.request
    logger.info(
        (
            f"Response event hook: {req.method} {req.url} - "
            f"Status {response.status_code} - "
            f"Response {response.read()}"
        )
    )


class MergeAPIClient:
    def __init__(self, credentials: MergeAPICredentials, logger: Logger):
        self.credentials = credentials
        self.logger = logger
        self.url = self.credentials["api_url"]
        self.client = httpx.Client(
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.credentials['authorization_token']}",
            },
            event_hooks={
                "request": [partial(log_request, self.logger)],
                "response": [partial(log_response, self.logger)],
            },
        )

    def _make_request(
        self, account_token: str, endpoint: str, params: QueryParams = {}
    ) -> httpx.Response:
        @retry(
            retry=retry_if_result(is_req_retriable),
            stop=stop.stop_after_attempt(get_maximum_request_attempts()),
            wait=wait.wait_exponential(multiplier=0.1, min=0, max=10),
            before=before.before_log(self.logger, self.logger.level),
            after=after.after_log(self.logger, self.logger.level),
            retry_error_callback=raise_client_api_exception,
        )
        def f() -> httpx.Response:
            return self.client.get(
                f"{self.url}{endpoint}",
                params=params,
                headers={"X-Account-Token": account_token},
            )

        return f()

    def fetch_all(self, account_token: str, endpoint: str) -> Iterator[Dict[str, Any]]:
        resp = self._make_request(account_token, endpoint, {"page_size": 100})
        content = resp.json()

        yield from content.get("results", [])

        cursor = content.get("next", None)
        while cursor:
            resp = self._make_request(
                account_token, endpoint, {"cursor": cursor, "page_size": 100}
            )
            content = resp.json()

            yield from content.get("results", [])

            cursor = content.get("next", None)


def client_factory(credentials: MergeAPICredentials, logger: Logger) -> MergeAPIClient:
    return MergeAPIClient(credentials=credentials, logger=logger)
