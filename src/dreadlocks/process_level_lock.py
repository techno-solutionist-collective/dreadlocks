from contextlib import contextmanager

from .globals import process_level_lock_ref


@contextmanager
def process_level_lock(
    fd: int, shared: bool = False, blocking: bool = True, reentrant: bool = False
):
    with process_level_lock_ref(fd) as ref:
        with ref.lock(shared, blocking, reentrant):
            yield
