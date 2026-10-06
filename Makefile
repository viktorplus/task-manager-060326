VENV ?= .venv
PYTHON ?= $(VENV)/bin/python
UV ?= uv

.PHONY: help install run check test migrate makemigrations shell freeze

help:
	@echo "Available commands:"
	@echo "  make install        Create .venv and install dependencies"
	@echo "  make run            Start the Django development server"
	@echo "  make check          Run Django system checks"
	@echo "  make test           Run the test suite"
	@echo "  make migrate        Apply database migrations"
	@echo "  make makemigrations Create new migrations"
	@echo "  make shell          Open the Django shell"
	@echo "  make freeze         Update requirements.txt from .venv"

install:
	$(UV) venv $(VENV)
	$(UV) pip install --python $(PYTHON) -r requirements.txt

run:
	$(PYTHON) manage.py runserver

check:
	$(PYTHON) manage.py check

test:
	$(PYTHON) manage.py test

migrate:
	$(PYTHON) manage.py migrate

makemigrations:
	$(PYTHON) manage.py makemigrations

shell:
	$(PYTHON) manage.py shell

freeze:
	$(UV) pip freeze --python $(PYTHON) > requirements.txt
