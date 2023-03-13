from functools import partial, wraps
from logging import Logger
from typing import Any, Callable

from chalicelib import config
from chalicelib.adapters import clients, repositories, storage
from chalicelib.utils import iterables

C = Callable[..., Any]

STORAGE_CLIENT_FACTORY = partial(
    storage.client_factory, config.get_storage_credentials()
)

MERGE_CLIENT_FACTORY = partial(
    clients.merge.client_factory,
    config.get_merge_api_credentials(),
)


class UnitOfWork:
    def __init__(
        self,
        logger: Logger,
        storage_client_factory: C = STORAGE_CLIENT_FACTORY,
    ):
        self.logger = logger
        self._storage_client_factory = storage_client_factory

    def __enter__(self) -> "UnitOfWork":
        self._storage = self._storage_client_factory()

        self.files = repositories.StorageRepository(self._storage)
        self.merge = MERGE_CLIENT_FACTORY(self.logger)

        return self

    def __exit__(self, *args, **kwargs):
        pass


def atomicness(_func) -> Callable:
    """Allow a function using an UnitOfWork instance to skip using the with statement"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw) -> Any:
            kwarg = iterables.find(
                kw.values(), fn=lambda kwarg: isinstance(kwarg, UnitOfWork)
            )
            arg = iterables.find(args, fn=lambda arg: isinstance(arg, UnitOfWork))

            assert (  # nosec B101
                arg or kwarg
            ), "Make sure that an instance of UnitOfWork is present as an argument"

            with arg or kwarg:  # pyright: ignore [reportOptionalContextManager]
                return func(*args, **kw)

        return wrapper

    return decorator(_func)
