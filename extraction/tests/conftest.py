import json
import os
import sys
from http import HTTPStatus
from os.path import abspath, dirname, join
from typing import Generator
from urllib.parse import urlencode

import boto3
import freezegun
import pytest
import responses
from chalice.app import Chalice
from chalice.test import Client
from moto import mock_s3
from pytest_httpx import HTTPXMock

import app
from chalicelib.adapters import storage as storage_adapter
from chalicelib.config import get_merge_api_credentials, get_storage_credentials

BASE_DIR = dirname(dirname(abspath(__file__)))

sys.path.insert(0, os.path.join(BASE_DIR, "./"))


@pytest.fixture
def test_app() -> Chalice:
    return app.app


@pytest.fixture
def client(test_app: Chalice) -> Generator[Client, None, None]:
    with Client(test_app) as client:
        yield client


@pytest.fixture(autouse=True)
def bucket():
    credentials = get_storage_credentials()
    with mock_s3():
        boto3.resource("s3").create_bucket(
            Bucket=credentials["aws_storage_bucket_name"]
        )
        yield storage_adapter.client_factory(credentials)


@pytest.fixture
def freeze():
    "Ensure that params are encoded using the same datetime"

    with freezegun.freeze_time("2023-03-13T00:00:01+00:00") as freezed_time:
        yield freezed_time


@pytest.fixture
def mocked_response(httpx_mock: HTTPXMock):
    yield httpx_mock


@pytest.fixture
def make_cloudwatch_scheduled_event():
    def _make_cloudwatch_event(client: Client):
        return client.events.generate_cw_event(
            source="aws.events",
            detail_type="Scheduled Event",
            detail={},
            resources=[
                "arn:aws:events:us-east-1:123456789012:rule/testevents-dev-every_minute"
            ],
        )

    return _make_cloudwatch_event


@pytest.fixture
def mock_merge_roster_response(mocked_response):
    cred = get_merge_api_credentials()

    def f(
        data,
        query_params,
        status_code=HTTPStatus.OK,
    ):
        mocked_response.add_response(
            method=responses.GET,
            url=f"{cred['api_url']}hris/v1/employees?{urlencode(query_params)}",
            json=data,
            status_code=status_code,
        )

    return f


@pytest.fixture
def mocked_merge_roster_response(mock_merge_roster_response, merge_roster):
    mock_merge_roster_response(data=merge_roster, query_params={"page_size": 100})


@pytest.fixture
def merge_roster():
    with open(join(BASE_DIR, "tests/mocks/merge/roster.json")) as f:
        return json.load(f)
