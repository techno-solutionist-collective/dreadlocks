Usage
=====

.. _installation:

Installation
------------

To use :mod:`dreadlocks`, first install it using pip:

.. code-block:: console

   (.venv) $ pip install dreadlocks

Using `dreadlocks`
------------------

Public API members are :func:`dreadlocks.path_lock`,
:func:`dreadlocks.process_level_path_lock`,
:func:`dreadlocks.thread_level_path_lock`,
:class:`dreadlocks.AcquiringLockWouldBlockError`,
:class:`dreadlocks.AcquiringProcessLevelLockWouldBlockError`,
:class:`dreadlocks.AcquiringThreadLevelLockWouldBlockError`,
:class:`dreadlocks.RecursiveDeadlockError`.

>>> from dreadlocks import path_lock, ...

To blockingly acquire an exclusive non-reentrant global (thread-level and
process-level) lock on file named `.lock`, use :func:`dreadlocks.path_lock` as
follows:

>>> with path_lock('.lock'):
>>>   ...

Note that attempting to acquire a non-reentrant lock may raise
:class:`dreadlocks.RecursiveDeadlockError`.

Exclusivity, blockingness, and reentrancy are all configurable through
flags:

>>> with path_lock('.lock', shared=True, blocking=False, reentrant=True):
>>>   ...

Note that attempting to acquire a lock non-blockingly may raise
:class:`dreadlocks.AcquiringLockWouldBlockError`.

:func:`dreadlocks.process_level_path_lock` and :func:`dreadlocks.thread_level_path_lock` have similar
APIs. In fact, :func:`dreadlocks.path_lock` is made out of the composition of those two
lower-level constructs.  One notable difference is that
:func:`dreadlocks.thread_level_path_lock` will not create a lock file.
