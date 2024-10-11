DOCKER_COMPOSE := deploy/docker-compose.yml
DOCKER_ENV := deploy/.env
DOCKER_COMPOSE_RUNNER := docker-compose
PROJECT_NAME := api
ALEMBIC_CONFIG_FILE := api/config/alembic.ini

ifeq ($(ENV),docker)
	DOCKER_ENV := deploy/.env.dev
	include $(DOCKER_ENV)
	export $(shell sed 's/=.*//' $(DOCKER_ENV))
else ifeq ($(ENV),local)
	DOCKER_ENV := deploy/.env.dev.local
	include $(DOCKER_ENV)
	export $(shell sed 's/=.*//' $(DOCKER_ENV))
endif

.PHONY: backend_run
backend_run:
	poetry run gunicorn api.presentation.api.main:app --reload -b $(HOST):$(BACKEND_PORT) \
	--worker-class uvicorn.workers.UvicornWorker \
	--log-level $(LOG_LEVEL)

.PHONY: backend_run_dev
backend_run_dev:
	poetry run uvicorn api.presentation.api.main:app --port $(BACKEND_HOST_PORT) --reload 

.PHONY: migrate_create
migrate_create:
	poetry run alembic -c $(ALEMBIC_CONFIG_FILE) revision --autogenerate

.PHONY: migrate_up
migrate_up:
	poetry run alembic -c $(ALEMBIC_CONFIG_FILE) upgrade head

.PHONY: migrate_downgrade
migrate_downgrade:
	poetry run alembic -c $(ALEMBIC_CONFIG_FILE) downgrade $(VERSION)

.PHONY: compose_up
compose_up:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) -p $(PROJECT_NAME) up -d

.PHONY: compose_build
compose_build:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) -p $(PROJECT_NAME) build

.PHONY: compose_down
compose_down:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) -p $(PROJECT_NAME) down

.PHONY: compose_logs
compose_logs:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) -p $(PROJECT_NAME) logs -f

.PHONY: precommit
precommit: format lint precommit_tests

.PHONY: format
format:
	@echo "------- Formatting code with Black -------"
	@black .
	@echo ""

	@echo "------- Formatting imports with Isort -------"
	@isort .
	@echo ""

.PHONY: lint
lint:
	@echo "------- Checking code style with Flake8 -------"
	@flake8 .
	@echo ""

.PHONY: tests
tests:
	@echo "------- Running test -------"
	@poetry run pytest

.PHONY: tests_one_fail
tests_one_fail:
	@echo "------- Running test -------"
	@poetry run pytest -s --lf --maxfail=1

.PHONY: tests_durations
tests_durations:
	@echo "------- Running test -------"
	@poetry run pytest --durations=10 --tb=no
	@echo ""

.PHONY: precommit_tests
precommit_tests:
	@echo "------- Running precommit tests with pytest -------"
	@poetry run pytest -q
	@echo ""

.PHONY: build_docker_image_for_ci_cd
build_docker_image_for_ci_cd:
	docker build --platform linux/amd64 -t mihey83/container_for_ci_cd:latest -f "./deploy/DockerfileForCICD" .