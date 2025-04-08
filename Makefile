PACKAGES := clinicadl-zoo
POETRY ?= poetry
CONDA ?= conda
CONDA_ENV ?= "./env"

.PHONY: help
help: Makefile
	@echo "Commands:"
	@sed -n 's/^##//p' $<

.PHONY: check.lock
check.lock:
	@$(POETRY) check --lock

## build			: Build the package.
.PHONY: build
build:
	@$(POETRY) build

.PHONY: clean.test
clean.test:
	@$(RM) -r .pytest_cache/

## env			: Bootstrap an environment.
.PHONY: env
env: env.dev

.PHONY: env.conda
env.conda:
	@$(CONDA) env create -p $(CONDA_ENV)

.PHONY: env.dev
env.dev:
	@$(POETRY) install


## format			: Format the codebase.
.PHONY: format
format: format.black format.isort

.PHONY: format.black
format.black: env.dev
	@$(POETRY) run black --quiet $(PACKAGES)

.PHONY: format.isort
format.isort: env.dev
	@$(POETRY) run isort --quiet $(PACKAGES)

## lint			: Lint the codebase.
.PHONY: lint
lint: lint.black lint.isort

.PHONY: lint.black
lint.black: env.dev
	@$(POETRY) run black --check --diff $(PACKAGES)

.PHONY: lint.isort
lint.isort: env.dev
	@$(POETRY) run isort --check --diff $(PACKAGES)

## Install
.PHONY: install
install: check.lock
	@$(POETRY) install

.PHONY: install.dev
install.dev: check.lock
	@$(POETRY) install --only dev
	

## tests        : Run the unit tests
.PHONY: test
test: install
	@$(POETRY) run python -m pytest -v tests/unittests
