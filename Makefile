.PHONY: i
i: install

.PHONY: install
install: .venv

.venv: poetry.toml pyproject.toml
	poetry install --with dev --with test --with type
	@touch .venv


.PHONY: lock
lock: poetry.lock

poetry.lock: poetry.toml pyproject.toml
	poetry lock --no-update
	@touch poetry.lock


.PHONY: install-git-hooks
install-git-hooks:
	poetry run pre-commit install
