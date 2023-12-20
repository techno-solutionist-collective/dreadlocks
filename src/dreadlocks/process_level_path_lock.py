from contextlib import contextmanager
from os.path import normpath

from .globals import fd_ref
from .process_level_lock import process_level_lock


@contextmanager
def _process_level_path_lock(
    normalized_path: str, shared: bool = False, blocking: bool = True, reentrant: bool = False
):
    with fd_ref(normalized_path) as fd:
        with process_level_lock(fd, shared, blocking, reentrant):
            yield fd


def process_level_path_lock(
    path: str, shared: bool = False, blocking: bool = True, reentrant: bool = False
):
    """Locks a path at the process-level.

    Parameters
    ----------
    path
        The path to lock. This path is open in write mode to ensure its
        existence in an atomic way. Cannot be a path to an existing directory.
        The path is normalized so that the underlying file descriptor can be
        keyed.
    shared
        Whether the lock is shared. If not shared, the lock is
        exclusive. One can have either no locks, a single exclusive lock,
        or any positive number of shared locks on the same resource at any given
        time.
    blocking
        Whether lock acquisition is blocking. If True, will raise an
        error if a lock cannot be acquired immediately. Otherwise, will block
        until the lock is acquired.
    reentrant
        Whether lock acquisition is reentrant. If True, allows to lock
        recursively. Otherwise, locking recursively results in a dead-lock.
    """
    normalized_path = normpath(path)
    return _process_level_path_lock(normalized_path, shared, blocking, reentrant)
