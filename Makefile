# -------------------------------
# DebateBot - Makefile
# -------------------------------

# Tools
PYTHON      ?= python3
PIP         ?= pip3
VENVDIR     ?= .venv
ACTIVATE    := $(VENVDIR)/bin/activate
COMPOSE     ?= docker compose

# Helper: colored echo
YELLOW=\033[1;33m
GREEN=\033[1;32m
RED=\033[1;31m
NC=\033[0m

# Default target: show help
.PHONY: help
help:
	@echo ""
	@echo "DebateBot — available make commands"
	@echo "-----------------------------------"
	@echo "make            Show this help"
	@echo "make install    Create venv and install Python deps locally"
	@echo "make test       Run tests (pytest)"
	@echo "make run        Run the service (API + Redis) with Docker Compose"
	@echo "make down       Stop services started by Docker Compose"
	@echo "make clean      Stop & remove all Compose containers, networks, and volumes"
	@echo ""

# Alias
.PHONY: default
default: help

# ---- tool checks -------------------------------------------------------------

.PHONY: _check_python
_check_python:
	@command -v $(PYTHON) >/dev/null 2>&1 || { \
		echo "$(RED)ERROR$(NC): python3 not found."; \
		echo "Install Python 3.10+ from https://www.python.org/downloads/"; \
		exit 1; }

.PHONY: _check_pip
_check_pip:
	@command -v $(PIP) >/dev/null 2>&1 || { \
		echo "$(RED)ERROR$(NC): pip3 not found."; \
		echo "Install pip: https://pip.pypa.io/en/stable/installation/"; \
		exit 1; }

.PHONY: _check_docker
_check_docker:
	@command -v docker >/dev/null 2>&1 || { \
		echo "$(RED)ERROR$(NC): Docker not found."; \
		echo "Install Docker Desktop: https://docs.docker.com/get-docker/"; \
		exit 1; }

.PHONY: _check_compose
_check_compose: _check_docker
	@docker version >/dev/null 2>&1 || { \
		echo "$(RED)ERROR$(NC): Docker daemon not running."; \
		echo "Start Docker Desktop and try again."; \
		exit 1; }
	@$(COMPOSE) version >/dev/null 2>&1 || { \
		echo "$(RED)ERROR$(NC): docker compose plugin not found."; \
		echo "Update Docker Desktop or install Compose v2: https://docs.docker.com/compose/"; \
		exit 1; }

# ---- local install & tests ---------------------------------------------------

.PHONY: install
install: _check_python _check_pip
	@echo "$(YELLOW)>>> Creating virtualenv: $(VENVDIR)$(NC)"
	@$(PYTHON) -m venv $(VENVDIR)
	@echo "$(YELLOW)>>> Upgrading pip$(NC)"
	@. $(ACTIVATE) && pip install --upgrade pip
	@echo "$(YELLOW)>>> Installing requirements.txt$(NC)"
	@. $(ACTIVATE) && pip install -r requirements.txt
	@echo "$(GREEN)✔ Local environment ready. Activate with: source $(VENVDIR)/bin/activate$(NC)"

.PHONY: test
test: _check_python
	@if [ ! -d "$(VENVDIR)" ]; then \
		echo "$(YELLOW)>>> No venv found; running tests with system python$(NC)"; \
	fi
	@echo "$(YELLOW)>>> Running pytest$(NC)"
	@. $(ACTIVATE) 2>/dev/null || true; pytest -q || { echo "$(RED)Tests failed$(NC)"; exit 1; }

# ---- docker orchestration ----------------------------------------------------

.PHONY: run
run: _check_compose
	@echo "$(YELLOW)>>> Building & starting DebateBot (API + Redis)$(NC)"
	@$(COMPOSE) up --build -d
	@echo "$(GREEN)✔ Running$(NC)."
	@echo "Health check:  curl -s http://localhost:8080/health"

.PHONY: down
down: _check_compose
	@echo "$(YELLOW)>>> Stopping services$(NC)"
	@$(COMPOSE) down

.PHONY: clean
clean: _check_compose
	@echo "$(YELLOW)>>> Removing containers, networks, and anonymous volumes$(NC)"
	@$(COMPOSE) down -v --remove-orphans
	@echo "$(GREEN)✔ Cleaned$(NC)"
