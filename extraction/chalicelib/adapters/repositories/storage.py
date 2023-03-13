from typing import IO

from chalicelib.adapters.storage import StorageClient, StorageWaiterException
from chalicelib.domain.fields.datetime import rfc3339_utc_now_formatted_datetime


class FileNotFoundException(Exception):
    pass


class StorageRepository:
    def __init__(self, storage: StorageClient):
        self._storage = storage

    def upload_to(self, fileobj: IO, key: str) -> dict:
        self._storage.upload_fileobj(Fileobj=fileobj, Key=key)
        return self._wait_until_exists(key)

    def _wait_until_exists(self, key: str) -> dict:
        try:
            self._storage.Object(key).wait_until_exists()
        except StorageWaiterException as exc:
            return {
                rfc3339_utc_now_formatted_datetime(): {
                    **exc.last_response,
                    **exc.kwargs,
                }
            }
        else:
            return {}
