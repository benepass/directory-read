from logging import INFO
from typing import Optional, TypedDict

import sentry_sdk
from decouple import config
from sentry_sdk import init as init_sentry
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from sentry_sdk.integrations.chalice import ChaliceIntegration

DEV = "dev"
TEST = "test"


def get_environment() -> str:
    if config("TESTING", default=False):
        return TEST

    return config("ENVIRONMENT", default=DEV).lower()


def get_sentry_dsn() -> str:
    return config("SENTRY_DSN", default="")


def get_app_name() -> str:
    return "directory-read/extraction"


def is_debug() -> bool:
    return bool(config("DEBUG", default=False, cast=bool))


def is_testing() -> bool:
    return get_environment() == TEST


def is_dev_or_test() -> bool:
    return get_environment() in [TEST, DEV]


def is_packaging() -> bool:
    """
    Some expensive operations does not need to run when the app is packaging
    """

    # Set as True by chalice cli
    return bool(config("AWS_CHALICE_CLI_MODE", default=False))


def get_log_level() -> int:
    return INFO  # Log info messages even when DEBUG is False


class InfrastructureCredentials(TypedDict):
    endpoint_url: Optional[str]


def get_infrastructure_credentials() -> InfrastructureCredentials:
    return {"endpoint_url": config("ENDPOINT_URL", default=None)}


class StorageCredentials(TypedDict):
    infrastructure_credentials: InfrastructureCredentials
    aws_storage_bucket_name: str


def get_storage_credentials() -> StorageCredentials:
    return {
        "infrastructure_credentials": get_infrastructure_credentials(),
        "aws_storage_bucket_name": config("AWS_STORAGE_BUCKET_NAME", default=""),
    }


def init_app_monitoring():
    init_sentry(
        dsn=get_sentry_dsn(),
        integrations=[ChaliceIntegration(), AwsLambdaIntegration(timeout_warning=True)],
        environment=get_environment(),
    )


def capture_monitored_exception(exp: BaseException):
    """Proxies sentry_sdk so that there is no need to import the library"""
    sentry_sdk.capture_exception(exp)


def get_maximum_request_attempts() -> int:
    """Tests shouldn't take too long"""
    return 5 if not is_testing() else 2


def get_cognito_jwks_uri() -> str:
    return str(config("COGNITO_JWKS_URI", default=""))
