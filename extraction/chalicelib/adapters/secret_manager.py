import json
from typing import TYPE_CHECKING

import boto3

from chalicelib.utils.laziness import lazy

if TYPE_CHECKING:
    from mypy_boto3_secretsmanager import Client

    SecretsManagerClient = Client
else:
    SecretsManagerClient = object


@lazy
def client_factory() -> SecretsManagerClient:
    return boto3.client(service_name="secretsmanager")


def get_secret(key: str) -> dict:
    return json.loads(client_factory().get_secret_value(SecretId=key)["SecretString"])
