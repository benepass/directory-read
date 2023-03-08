import os
import sys
from typing import Generator

import boto3
import freezegun
import pytest
from chalice.app import Chalice
from chalice.test import Client
from moto import mock_s3
from pytest_httpx import HTTPXMock

import app
from chalicelib.adapters import storage as storage_adapter
from chalicelib.config import get_storage_credentials

sys.path.insert(0, os.path.realpath("./"))


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

    with freezegun.freeze_time("2021-1-1T00:00:01+00:00") as freezed_time:
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
