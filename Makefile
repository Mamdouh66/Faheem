DOCKER_COMPOSE = docker-compose
SERVICE_NAME = app

COLOR_RESET = \033[0m
COLOR_GREEN = \033[32m
COLOR_BLUE = \033[34m
COLOR_YELLOW = \033[33m

.PHONY: help build up down logs clean run-flow install clean

help: ## Display this help
	@echo "$(COLOR_BLUE)Available targets:$(COLOR_RESET)"
	@awk 'BEGIN {FS = ":.*##"; printf "\n$(COLOR_BLUE)%-20s$(COLOR_RESET) $(COLOR_YELLOW)%s$(COLOR_RESET)\n", "Target", "Help"} \
		/^[a-zA-Z\._-]+:.*##/ { printf "$(COLOR_GREEN)%-20s$(COLOR_RESET) $(COLOR_YELLOW)%s$(COLOR_RESET)\n", $$1, $$2 } \
		/^##@/ { printf "\n$(COLOR_BLUE)%s$(COLOR_RESET)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

build: ## Build the Docker images
	@echo "$(COLOR_BLUE)Building Docker images...$(COLOR_RESET)"
	@$(DOCKER_COMPOSE) build
	@echo "$(COLOR_GREEN)Build completed successfully!$(COLOR_RESET)"

up: ## Start the Docker containers
	@echo "$(COLOR_BLUE)Starting Docker containers...$(COLOR_RESET)"
	@$(DOCKER_COMPOSE) up -d
	@echo "$(COLOR_GREEN)Containers are up and running!$(COLOR_RESET)"

down: ## Stop the Docker containers
	@echo "$(COLOR_BLUE)Stopping Docker containers...$(COLOR_RESET)"
	@$(DOCKER_COMPOSE) down
	@echo "$(COLOR_GREEN)Containers have been stopped!$(COLOR_RESET)"

logs: ## Display logs of the Docker containers
	@echo "$(COLOR_BLUE)Displaying Docker logs...$(COLOR_RESET)"
	@$(DOCKER_COMPOSE) logs -f $(SERVICE_NAME)

clean: ## Clean up Docker containers and images
	@echo "$(COLOR_BLUE)Cleaning up Docker containers and images...$(COLOR_RESET)"
	@$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans
	@echo "$(COLOR_GREEN)Cleanup completed!$(COLOR_RESET)"

run-flow: ## Run the MLflow server
	@echo "$(COLOR_BLUE)Starting MLflow server...$(COLOR_RESET)"
	@mlflow server -h 0.0.0.0 -p 8080 --backend-store-uri tmp/mlflow
	@echo "$(COLOR_GREEN)MLflow server is running!$(COLOR_RESET)"

install: ## Install Poetry and project dependencies
	@if ! command -v poetry &> /dev/null; then \
		echo "$(COLOR_YELLOW)Poetry not found. Installing Poetry...$(COLOR_RESET)"; \
		pip install poetry; \
	fi
	@echo "$(COLOR_GREEN)Poetry is installed.$(COLOR_RESET)"
	@poetry --version
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "$(COLOR_YELLOW)Not in a virtual environment. Creating a virtual environment with Poetry...$(COLOR_RESET)"; \
		poetry env use python3; \
	else \
		echo "$(COLOR_GREEN)Already in a virtual environment: $$VIRTUAL_ENV$(COLOR_RESET)"; \
	fi
	@echo "$(COLOR_BLUE)Installing dependencies from pyproject.toml...$(COLOR_RESET)"
	@poetry install
	@echo "$(COLOR_GREEN)Dependencies installed!$(COLOR_RESET)"

run: ## Run the FastAPI application (locally)
	@echo "$(COLOR_BLUE)Running the application...$(COLOR_RESET)"
	@fastapi dev faheem/server.py
	@echo "$(COLOR_GREEN)Application is running!$(COLOR_RESET)"

clean: ## Clean up the project directory
	@find . -type f -name "*.DS_Store" -ls -delete
	@find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	@find . | grep -E ".pytest_cache" | xargs rm -rf
	@find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	@rm -rf .coverage*
