.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: start
start: ## Start the application
	@docker compose up -d --build

.PHONY: stop
stop: ## Stop the application
	@docker compose stop

.PHONY: backend-lint
backend-lint: ## Lint the backend
	@docker compose run --rm backend sh -c "ruff format --check . && ruff check . --output-format=full"

.PHONY: backend-lint-fix
backend-lint-fix: ## Lint and fix the backend code
	@docker compose run --rm backend sh -c "ruff format . && ruff check . --fix"

.PHONY: backend-test
backend-test: ## Test the backend
	@docker compose run --rm backend pytest --no-cov-on-fail --cov

.PHONY: backend-bash
backend-bash: ## Shell into the backend
	@docker compose run -it --rm backend sh

.PHONY: backend-dbshell
dbshell: ## Start a psql shell
	@docker compose run -it --rm db psql -Utimed timed

.PHONY: shellplus
shellplus: ## Run shell_plus
	@docker compose run -it --rm backend ./manage.py shell_plus

.PHONY: makemigrations
makemigrations: ## Make django migrations
	@docker compose run --rm backend ./manage.py makemigrations

.PHONY: backend-migrate
migrate: ## Migrate django
	@docker compose run --rm backend ./manage.py migrate

.PHONY: backend-debug-backend
backend-debug-backend: ## Start backend container with service ports for debugging
	@docker compose run --use-aliases --service-ports backend

.PHONY: flush
flush: ## Flush database contents
	@docker compose run --rm backend ./manage.py flush --no-input

.PHONY: loaddata
loaddata: flush ## Loads test data into the database
	@docker compose run --rm backend ./manage.py loaddata timed/fixtures/test_data.json

.PHONY: frontend-lint
frontend-lint: ## Lint the frontend
	@cd frontend && pnpm run lint

.PHONY: frontend-lint-fix
frontend-lint-fix: ## Lint and fix the frontend
	@cd frontend && pnpm run lint:fix

.PHONY: frontend-test
frontend-test: ## Run frontend tests
	@cd frontend && pnpm run test
