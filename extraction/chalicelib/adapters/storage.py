from typing import TYPE_CHECKING

import boto3
from botocore.exceptions import WaiterError

from chalicelib.config import StorageCredentials
from chalicelib.utils.laziness import lazy

if TYPE_CHECKING:
    from mypy_boto3_s3.service_resource import Bucket

    StorageClient = Bucket
else:
    StorageClient = object


StorageWaiterException = WaiterError


@lazy
def client_factory(credentials: StorageCredentials) -> StorageClient:
    return boto3.resource(
        service_name="s3", **credentials["infrastructure_credentials"]
    ).Bucket(name=credentials["aws_storage_bucket_name"])
