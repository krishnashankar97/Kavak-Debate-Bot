.PHONY: help install test run down clean
help: ## show all commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

install: ## install local dev deps
	python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

test: ## run tests
	. .venv/bin/activate && pytest -q

run: ## run all services in Docker
	docker-compose up --build

down: ## stop services
	docker-compose down

clean: ## stop and remove containers
	docker-compose down -v --remove-orphans
