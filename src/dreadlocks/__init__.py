"""The :mod:`dreadlocks` module exposes three context manager functions:
:func:`path_lock<dreadlocks.path_lock>`,
:func:`process_level_path_lock<dreadlocks.process_level_path_lock>`, and
:func:`thread_level_path_lock<dreadlocks.thread_level_path_lock>`.

Exception classes are part of the public API.
Other exported functions are implementation details subject to change.

Caveats:
    If you need to lock multiple paths you should have a total order for each
    subset of paths that could be locked simultaneously by the same thread and
    call :func:`dreadlocks.path_lock` multiple times respecting this total
    order. For instance via resolved absolute path lexicographical order.

    The Linux implementation relies on :code:`fcntl`/:code:`lockf` which is
    infamous for being hard to work with: if you close any file descriptor for
    a given file in a given process, it will release the lock held by that
    process, even if the lock was acquired through a different file descriptor.
    So you cannot easily open a lock file for reading or writing without
    breaking the locking mechanism. We implement locks in a way that uses a
    single fd while a lock exists for a given (normalized) path. That fd is
    opened with :code:`O_RDWR` and is yielded by :func:`dreadlocks.path_lock`
    for convenience, but the user should take extra care not to close this fd,
    as it would release the lock. For instance, :code:`open` must be used with
    the :code:`closefd` flag as in :code:`open(fd, closefd=False)`. This makes
    writing to the lock file, or reading several times from the lock file, a
    bit challenging but not impossible (using :code:`fp.seek` and
    :code:`fp.truncate`).

    Another solution would be to use flock but since that can sometimes
    fallback to the :code:`fcntl`/:code:`lockf` implementation, we prefer to
    use the latter implementation directly, and workaround the limitations. See
    http://0pointer.de/blog/projects/locking.html.

    Currently, on Windows, at the process level, shared locks are "simulated" by
    exclusive locks. Implementing true shared locks on this platform would require
    depending on userland libraries. This would be necessary, for instance, in
    situations where multiple processes need to lock shared resources and
    communicate simultaneously about the state of those resources. Note that the
    problem in this particular example can be circumvented at the cost of
    efficiency, by simulating locked shared resources through multiple rounds of
    exclusively-locked resources plus communication. Currently we conclude
    that, it is enough for the implementation to be simple for Windows, and
    correct on UNIX.

    The current implementation may not even be correct on UNIX in the scenario
    discussed above: in a multi-process, multi-thread setting, if one thread of
    process A acquires an exlusive lock at the thread-level first, then
    attempts to exclusively acquire the process-level lock, that process-level
    lock may already be acquired as shared by a thread of another process B
    that is waiting on the other threads of A to run. And vice versa, if one
    thread of process A acquires an exclusive lock at the process-level first,
    then attempts to exclusively acquire the thread-level lock, that
    thread-level lock may already be acquired as shared by other threads of
    process A, but they are waiting on a thread of process B that is in turn
    waiting for the process-level lock to be downgraded to shared. So it seems
    that composing two isolated implementations, one for threads, one for
    processes, cannot work in these "share and communicate" scenarios. One
    solution is to forbid upgrade and downgrade of a process-level lock which
    would effectively be the same as having an all-or-nothing lock (either you
    lock at both levels or you do not).

    Currently, on Windows, at the process level, we attempt to lock the entire
    file by passing the largest possible value to :code:`mscvrt.locking`
    :code:`nbytes` argument. If we want this implementation to be correct, we
    would need to :code:`fo.seek(0)` before calling :code:`mscvrt.locking` then
    perhaps restore the seek position? Also the largest possible value is
    2^31-1 which might not be enough for files larger than 2GB. Again, we do
    not currently need this "functionality".

    It is currently not possible to specify a timeout for acquiring a lock. The
    only options currently are immediate failure or forever blocking.
"""

from .path_lock import path_lock
from .process_level_path_lock import process_level_path_lock
from .thread_level_path_lock import thread_level_path_lock
from .errors import (
    AcquiringLockWouldBlockError,
    AcquiringProcessLevelLockWouldBlockError,
    AcquiringThreadLevelLockWouldBlockError,
    RecursiveDeadlockError,
)

__all__ = [
    "path_lock",
    "process_level_path_lock",
    "thread_level_path_lock",
    "AcquiringLockWouldBlockError",
    "AcquiringProcessLevelLockWouldBlockError",
    "AcquiringThreadLevelLockWouldBlockError",
    "RecursiveDeadlockError",
]
