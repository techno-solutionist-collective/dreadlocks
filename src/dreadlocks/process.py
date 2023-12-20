from collections import Counter
from contextlib import contextmanager
from threading import Lock, get_ident

from .errors import RecursiveDeadlockError, AcquiringProcessLevelLockWouldBlockError
from .platform import is_windows, process_level_lock, process_level_unlock


class ShareableProcessLock:
    """Creates a process lock for a FD shared by all threads of a process"""

    def __init__(self, fd: int):
        self._fd = fd
        self._lock = Lock()
        self._shared_by: Counter[int] = Counter()
        self._exclusively_held_by: Counter[int] = Counter()

    @contextmanager
    def lock(self, shared: bool = False, blocking: bool = True, reentrant: bool = False):
        """Locks the scoped FD

        shared : bool
            Whether the lock should be shared. If not shared, the lock is
            exclusive. Exclusively locking a file only means that we want to
            exclude other processes from locking the same file: any number of
            threads of the same process can lock the same file both shared and
            exclusively simultaneously. We keep track of which threads are
            holding what kind of locks to upgrade the process lock from shared
            to exclusive and vice versa.
        blocking : bool
            Whether lock acquisition should be blocking. If True, will raise an
            error if a lock cannot be acquired immediately. Otherwise, will block
            until the lock can be acquired.
        reentrant : bool
            Whether lock acquisition is reentrant. If True, allows each thread
            to lock the file recursively. Otherwise, the same thread
            recursively locking dead-locks.
        """
        thread_id = get_ident()
        if self._lock.acquire(blocking=blocking):
            try:
                if not reentrant and (
                    self._shared_by[thread_id] or self._exclusively_held_by[thread_id]
                ):
                    raise RecursiveDeadlockError()

                is_held_shared = bool(self._shared_by)
                is_held_exclusively = bool(self._exclusively_held_by)
                is_held = is_held_shared or is_held_exclusively

                if not is_held or (is_held_shared and not shared and not is_windows):
                    # NOTE: We only lock when the first locking attempt is made, or
                    # if we want to upgrade the lock to an exclusive lock, but only on
                    # UNIX since current implementation always uses exclusive locks on
                    # Windows.
                    process_level_lock(self._fd, shared, blocking)

                if shared:
                    self._shared_by[thread_id] += 1
                else:
                    self._exclusively_held_by[thread_id] += 1
            finally:
                self._lock.release()
        else:
            raise AcquiringProcessLevelLockWouldBlockError()

        try:
            yield

        finally:
            with self._lock:
                if shared:
                    self._shared_by[thread_id] -= 1
                    if not self._shared_by[thread_id]:
                        del self._shared_by[thread_id]
                else:
                    self._exclusively_held_by[thread_id] -= 1
                    if not self._exclusively_held_by[thread_id]:
                        del self._exclusively_held_by[thread_id]

                is_held_shared = bool(self._shared_by)
                is_held_exclusively = bool(self._exclusively_held_by)
                is_held = is_held_shared or is_held_exclusively

                if not is_held:
                    # NOTE: We only release the lock once we have exhausted all
                    # locking attempts
                    process_level_unlock(self._fd)
                elif not is_held_exclusively and not shared and not is_windows:
                    # NOTE: We downgrade the lock from exclusive to shared if we
                    # are not on Windows and we just released an exclusive
                    # lock, and no exclusive lock is left.
                    process_level_lock(self._fd, shared=True, blocking=True)
