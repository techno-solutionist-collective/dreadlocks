from os.path import normpath

from .thread_level_lock import thread_level_lock


def thread_level_path_lock(
    path: str, shared: bool = False, blocking: bool = True, reentrant: bool = False
):
    """Locks a key at the thread-level.

    Parameters
    ----------
    path
        The path to lock. The path is normalized so that the underlying lock
        can be keyed.
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
    return thread_level_lock(normalized_path, shared, blocking, reentrant)
