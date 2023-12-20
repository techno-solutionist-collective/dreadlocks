from os import O_RDWR, open as _open, close as _close
from threading import Lock
from .pool import ThreadSafeKeyedRefPool
from .thread import ShareableThreadLock
from .process import ShareableProcessLock

thread_level_lock_ref: ThreadSafeKeyedRefPool[str, ShareableThreadLock] = ThreadSafeKeyedRefPool(
    Lock(), {}, lambda _: ShareableThreadLock()
)

process_level_lock_ref: ThreadSafeKeyedRefPool[int, ShareableProcessLock] = ThreadSafeKeyedRefPool(
    Lock(), {}, ShareableProcessLock
)

fd_ref: ThreadSafeKeyedRefPool[str, int] = ThreadSafeKeyedRefPool(
    Lock(), {}, lambda normalized_path: _open(normalized_path, O_RDWR), destructor=_close
)
