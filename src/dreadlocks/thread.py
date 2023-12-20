from collections import Counter
from contextlib import contextmanager
from threading import Condition, RLock, get_ident

from .errors import AcquiringThreadLevelLockWouldBlockError, RecursiveDeadlockError


class ShareableThreadLock:
    def __init__(self):
        """
        Examples
        --------
        >>> lock = ShareableThreadLock()
        >>> i = 1
        >>> with lock.lock():
        ...     i += 1
        >>> i
        2

        """
        self._condition = Condition(RLock())
        self._acquired_by: Counter[int] = Counter()

    def lock(self, shared: bool = False, blocking: bool = True, reentrant: bool = False):
        if shared:
            return self._lock_sh(blocking=blocking, reentrant=reentrant)
        else:
            return self._lock_ex(blocking=blocking, reentrant=reentrant)

    @contextmanager
    def _lock_sh(self, blocking: bool = True, reentrant: bool = False):
        thread_id = get_ident()
        if self._condition.acquire(blocking=blocking):
            try:
                if not reentrant and self._acquired_by[thread_id]:
                    raise RecursiveDeadlockError()
                self._acquired_by[thread_id] += 1
            finally:
                self._condition.release()
        else:
            raise AcquiringThreadLevelLockWouldBlockError()

        try:
            yield

        finally:
            self._condition.acquire(blocking=True)
            try:
                self._acquired_by[thread_id] -= 1
                if not self._acquired_by[thread_id]:
                    del self._acquired_by[thread_id]  # NOTE: GC
                    if not self._acquired_by:
                        self._condition.notify_all()
            finally:
                self._condition.release()

    @contextmanager
    def _lock_ex(self, blocking: bool = True, reentrant: bool = False):
        thread_id = get_ident()
        if self._condition.acquire(blocking=blocking):
            acquired = False
            try:
                this_thread_count = Counter({thread_id: self._acquired_by[thread_id]})
                if blocking:
                    # NOTE: We could use self._acquired_by != this_thread_count in
                    # Python >= 3.10
                    while self._acquired_by - this_thread_count:
                        self._condition.wait()
                else:
                    # NOTE: We could use self._acquired_by != this_thread_count in
                    # Python >= 3.10
                    if self._acquired_by - this_thread_count:
                        raise AcquiringThreadLevelLockWouldBlockError()

                # NOTE: The following check also works for Python < 3.10 because we
                # systematically get rid of zero-count entries.
                if self._acquired_by:
                    # NOTE: The following two checks can be replaced by
                    # assert self._acquired_by == this_thread_count
                    # in Python >= 3.10
                    assert len(self._acquired_by) == 1
                    assert self._acquired_by[thread_id] == this_thread_count[thread_id]
                    if not reentrant:
                        raise RecursiveDeadlockError()

                acquired = True
                self._acquired_by[thread_id] += 1

                yield

            finally:
                if acquired:
                    self._acquired_by[thread_id] -= 1
                    if not self._acquired_by[thread_id]:
                        del self._acquired_by[thread_id]  # NOTE: GC
                self._condition.release()
        else:
            raise AcquiringThreadLevelLockWouldBlockError()
