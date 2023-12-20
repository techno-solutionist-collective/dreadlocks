from contextlib import contextmanager

from .globals import thread_level_lock_ref


@contextmanager
def thread_level_lock(
    key: str, shared: bool = False, blocking: bool = True, reentrant: bool = False
):
    with thread_level_lock_ref(key) as ref:
        with ref.lock(shared, blocking, reentrant):
            yield
