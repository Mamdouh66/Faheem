run flow:
	mlflow server -h 0.0.0.0 -p 8080 --backend-store-uri tmp/mlflow

install:
	@if ! command -v poetry &> /dev/null; then \
		echo "Poetry not found. Installing Poetry..."; \
		pip install poetry; \
	fi
	@echo "Poetry is installed."
	@poetry --version
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Not in a virtual environment. Creating a virtual environment with Poetry..."; \
		poetry env use python3; \
	else \
		echo "Already in a virtual environment: $$VIRTUAL_ENV"; \
	fi
	@echo "Installing dependencies from pyproject.toml..."
	@poetry install