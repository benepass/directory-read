import json
from contextlib import contextmanager
from tempfile import TemporaryFile
from typing import Any, Iterable


@contextmanager
def bufferize(rows: Iterable[Any]):
    with TemporaryFile() as buffer:
        buffer.write(json.dumps(rows).encode("utf-8"))
        buffer.seek(0)
        yield buffer
