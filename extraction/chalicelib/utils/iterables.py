from typing import Any, Callable, Iterable, Optional


def find(
    iterable: Iterable, *, fn: Callable[[Iterable], bool], default: Any = None
) -> Optional[Any]:
    return next((k for k in iterable if fn(k)), default)
