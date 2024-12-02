from contextlib import contextmanager

# from threading import get_ident

from .globals import thread_level_lock_ref


@contextmanager
def thread_level_lock(
    key: str, shared: bool = False, blocking: bool = True, reentrant: bool = False
):
    # print("CALL thread_level_lock (id={}, key={}, shared={}, blocking={}, reentrant={})".format(get_ident(), key, shared, blocking, reentrant))
    with thread_level_lock_ref(key) as ref:
        # print("REF thread_level_lock (id={}, key={}, shared={}, blocking={}, reentrant={})".format(get_ident(), key, shared, blocking, reentrant))
        with ref.lock(shared, blocking, reentrant):
            # print("YIELD thread_level_lock (id={}, key={}, shared={}, blocking={}, reentrant={})".format(get_ident(), key, shared, blocking, reentrant))
            yield
            # print("DONE thread_level_lock (id={}, key={}, shared={}, blocking={}, reentrant={})".format(get_ident(), key, shared, blocking, reentrant))
