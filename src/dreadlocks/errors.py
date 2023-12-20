class AcquiringLockWouldBlockError(Exception):
    """Raised when acquiring lock would block and blocking is False"""


class AcquiringProcessLevelLockWouldBlockError(AcquiringLockWouldBlockError):
    """Raised when acquiring a process-level lock would block and blocking is False"""


class AcquiringThreadLevelLockWouldBlockError(AcquiringLockWouldBlockError):
    """Raised when acquiring a thread-level lock would block and blocking is False"""


class RecursiveDeadlockError(Exception):
    """Raised when recursive dead-lock is detected."""
