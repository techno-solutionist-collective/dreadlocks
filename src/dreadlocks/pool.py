from contextlib import contextmanager
from typing import Generic, TypeVar, Callable, Optional
from threading import Lock

K = TypeVar("K")
V = TypeVar("V")


class ThreadSafeKeyedRefPool(Generic[K, V]):
    def __init__(
        self,
        lock: Lock,
        refs: dict[K, tuple[V, int]],
        factory: Callable[[K], V],
        destructor: Optional[Callable[[V], None]] = None,
    ):
        self._lock = lock
        self._refs = refs
        self._factory = factory
        self._destructor = destructor

    @contextmanager
    def __call__(self, key: K):
        with self._lock:
            entry = self._refs.get(key)
            if entry is None:
                # NOTE: We create a new object if none exists
                obj = self._factory(key)
                self._refs[key] = (obj, 1)
            else:
                # NOTE: Otherwise we count one ref more
                (obj, refcount) = entry
                self._refs[key] = (obj, refcount + 1)

        try:
            yield obj

        finally:
            with self._lock:
                (_, refcount) = self._refs[key]
                if refcount == 1:
                    # NOTE: We remove the object from the pool since nobody
                    # else holds a reference to it.
                    del self._refs[key]
                    if self._destructor is not None:
                        self._destructor(obj)
                else:
                    # NOTE: Otherwise we count one ref less
                    self._refs[key] = (obj, refcount - 1)
