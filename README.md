🔒 `dreadlocks`
[![PyPI - Version](https://img.shields.io/pypi/v/dreadlocks?style=flat)](https://pypi.org/project/dreadlocks)
[![Codecov](https://img.shields.io/codecov/c/github/techno-solutionist-collective/dreadlocks?style=flat)](https://app.codecov.io/gh/techno-solutionist-collective/dreadlocks)
==

> A cross-platform file-locking software library for Python that supports
> thread-level locks, process-level locks, and both simultaneously.


## 📚 Documentation

See [GitHub pages](https://techno-solutionist-collective.github.io/dreadlocks/latest):

  - [Usage](https://techno-solutionist-collective.github.io/dreadlocks/latest/usage)
  - [API reference](https://techno-solutionist-collective.github.io/dreadlocks/latest/api)



## 👩‍💻  Development

The only external requirements are Python and `poetry`.

`poetry` takes care of setting up a minimal environment with `tox` and `pre-commit` installed.
For that run:

```sh
poetry install --only dev
```

All other environments are managed by `tox` (and uses `poetry` internally).


### 👕 Lint

```sh
poetry run tox -e lint-check
```

> :information_source: Some linting errors can be automatically fixed with
> `poetry run tox -e lint`.


### ☑️ Type check

```sh
poetry run tox -e type-check
```


### 🧪 Tests

> :information_source: Add the `-cover` suffix to generate coverage
> information.

#### 📦 Unit tests

```sh
poetry run tox -e unit
```

#### 📑 Doctests

```sh
poetry run tox -e doctest
```


#### ☔ Coverage

If tests have been run with the `-cover` suffix, coverage reports can be
generated with `poetry run tox -e coverage`.

The HTML coverage report can be served to port `8000` with `poetry run tox -e
coverage-serve`.


### 📜 Dependencies licenses

Dependencies licenses can be checked with `poetry run tox -e licenses`.


### ⚖️ Licensing

This software library is triple-licensed under the BSD 2-clause, LGPLv3 or
later, and GPLv3 or later.

You must choose to be bound by at least one of these licenses when you use
this work.

`SPDX-License-Identifier: BSD-2-Clause OR LGPL-3.0-or-later OR GPL-3.0-or-later`


## 👀 See also

  - [On the Brokenness of File Locking](http://0pointer.de/blog/projects/locking) by [Lennart Poettering](http://0pointer.de).
  - [Addendum on the Brokenness of File Locking](http://0pointer.de/blog/projects/locking2) by [Lennart Poettering](http://0pointer.de).
