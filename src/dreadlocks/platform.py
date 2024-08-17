import os
import sys

from .errors import AcquiringProcessLevelLockWouldBlockError

is_windows = os.name == "nt"
is_mac_os = sys.platform == "darwin"


if is_windows:
    # Windows file locking
    import msvcrt

    # NOTE: lock the entire file
    _lock_length = -1 if sys.version_info.major == 2 else int(2**31 - 1)

    def _is_process_level_lock_timeout_error(error: OSError) -> bool:
        """Check if an OSError corresponds to a blocking lock timeout error

        Note that the errno for a non-blocking lock failure would be 13 with a
        strerror of "Permission denied".
        """
        return error.errno == 36 and error.strerror == "Resource deadlock avoided"

    def _is_process_level_lock_blocking_error(error: OSError) -> bool:
        """Check that an OSError corresponds to an error raised because
        a process-level lock cannot be acquired immediately
        """
        return (
            isinstance(error, PermissionError)
            and error.errno == 13
            and error.strerror == "Permission denied"
        )

    def process_level_lock(fd: int, shared: bool = False, blocking: bool = True):
        # NOTE: Simulates shared lock using an exclusive lock. This
        # implementation does not allow to lock the same fd multiple times.
        # This does not matter as we make sure not to do that.
        if blocking:
            while True:
                try:
                    msvcrt.locking(  # type: ignore [reportGeneralTypeIssues, reportUnknownMemberType]
                        fd,
                        msvcrt.LK_LOCK,  # type: ignore [reportGeneralTypeIssues, reportUnknownMemberType]
                        _lock_length,
                    )
                    break
                except OSError as error:
                    if not _is_process_level_lock_timeout_error(error):
                        raise error
        else:
            try:
                msvcrt.locking(  # type: ignore [reportGeneralTypeIssues, reportUnknownMemberType]
                    fd,
                    msvcrt.LK_NBLCK,  # type: ignore [reportGeneralTypeIssues, reportUnknownMemberType]
                    _lock_length,
                )
            except PermissionError as error:
                if _is_process_level_lock_blocking_error(error):
                    raise AcquiringProcessLevelLockWouldBlockError()
                else:
                    raise error

    def process_level_unlock(fd: int):
        # NOTE: This implementation (Windows) will raise an error if attempting
        # to unlock an already unlocked fd. This does not matter as we make
        # sure not to do that.
        msvcrt.locking(  # type: ignore [reportGeneralTypeIssues, reportUnknownMemberType]
            fd,
            msvcrt.LK_UNLCK,  # type: ignore [reportGeneralTypeIssues, reportUnknownMemberType]
            _lock_length,
        )

else:
    # UNIX based file locking
    import fcntl

    def _is_process_level_lock_blocking_error(error: OSError) -> bool:
        """Check that an OSError corresponds to an error raised because
        a process-level lock cannot be acquired immediately
        """
        return (
            isinstance(error, BlockingIOError)
            and (
                (is_mac_os and error.errno == 35)  # MacOS
                or (not (is_mac_os) and error.errno == 11)  # Linux
            )
            and error.strerror == "Resource temporarily unavailable"
        )

    def process_level_lock(fd: int, shared: bool = False, blocking: bool = True):
        operation = fcntl.LOCK_SH if shared else fcntl.LOCK_EX
        if blocking:
            while True:
                try:
                    fcntl.lockf(fd, operation)
                    break
                except OSError as error:
                    if (
                        not is_mac_os
                        and error.errno == 35
                        and error.strerror == "Resource deadlock avoided"
                    ):
                        # From man fcntl(2)
                        # Deadlock detection The deadlock-detection algorithm
                        # employed by the kernel when dealing with F_SETLKW
                        # requests can yield both false negatives (failures to
                        # detect deadlocks, leaving a set of deadlocked
                        # processes blocked indefinitely) and false positives
                        # (EDEADLK errors when there is no deadlock).  For ex‐
                        # ample,  the kernel limits the lock depth of its
                        # dependency search to 10 steps, meaning that circular
                        # deadlock chains that exceed that size will not be
                        # detected.  In addition, the kernel may falsely
                        # indicate a deadlock when two or more processes
                        # created  using  the clone(2) CLONE_FILES flag place
                        # locks that appear (to the kernel) to conflict.
                        pass
                    else:
                        raise

        else:
            try:
                fcntl.lockf(fd, operation | fcntl.LOCK_NB)
            except BlockingIOError as error:
                if _is_process_level_lock_blocking_error(error):
                    raise AcquiringProcessLevelLockWouldBlockError()
                else:
                    raise error

    def process_level_unlock(fd: int):
        # NOTE: This implementation (UNIX) will NOT raise an error if attempting
        # to unlock an already unlocked fd. This does not matter as we make
        # sure not to do that.
        fcntl.lockf(fd, fcntl.LOCK_UN)
