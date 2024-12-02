from contextlib import contextmanager

# from threading import get_ident

from .globals import process_level_lock_ref


@contextmanager
def process_level_lock(
    fd: int, shared: bool = False, blocking: bool = True, reentrant: bool = False
):
    # print("CALL process_level_lock (id={}, fd={}, shared={}, blocking={}, reentrant={})".format(get_ident(), fd, shared, blocking, reentrant))
    with process_level_lock_ref(fd) as ref:
        # print("REF process_level_lock (id={}, fd={}, shared={}, blocking={}, reentrant={})".format(get_ident(), fd, shared, blocking, reentrant))
        with ref.lock(shared, blocking, reentrant):
            # print("YIELD process_level_lock (id={}, fd={}, shared={}, blocking={}, reentrant={})".format(get_ident(), fd, shared, blocking, reentrant))
            yield
            # print("DONE process_level_lock (id={}, fd={}, shared={}, blocking={}, reentrant={})".format(get_ident(), fd, shared, blocking, reentrant))
