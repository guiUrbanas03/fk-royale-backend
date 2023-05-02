-include .env
export

SOURCE := source
TESTS := tests
CONFIG := config
PYTHON_FILES := ${SOURCE} ${TESTS} ${CONFIG}
LINE_LENGTH := 79
DOCKER_IMAGE_NAME := fk-royale-flask
APP_LOCATION := ${SOURCE}:create_app
APP_COMMANDS_LOCATION := docker exec ${DOCKER_IMAGE_NAME} flask --app ${APP_LOCATION}

.PHONY: *


run:
	docker compose up
shell:
	poetry shell

app-bash:
	docker exec -it ${DOCKER_IMAGE_NAME} bash

format:
	autoflake --in-place --remove-unused-variables --remove-all-unused-imports --ignore-init-module-imports -r ${PYTHON_FILES}
	isort ${PYTHON_FILES}
	black ${PYTHON_FILES}

format-check:
	isort --check-only ${PYTHON_FILES}
	black --diff --check ${PYTHON_FILES}
	docformatter --check --recursive ${PYTHON_FILES}
	pylint ${SOURCE}

flake8:
	flake8 source --extend-ignore=E203,E501 --per-file-ignores="__init__.py:F401"

format-all:
	make format format-check flake8

docker-run:
	docker run --rm \
		-p 8000:8000 \
		-v $(PWD):/app \
		--name ${DOCKER_IMAGE_NAME} ${DOCKER_IMAGE_NAME}

migrate-db:
	alembic upgrade head

seed-db:
	${APP_COMMANDS_LOCATION} seed-db

setup-app:
	make migrate-db seed-db