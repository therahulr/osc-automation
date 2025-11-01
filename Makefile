SHELL := /bin/zsh

.PHONY: help install setup run-osc-login fmt lint typecheck clean

help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies and Playwright browsers
	@echo "Installing Python dependencies..."
	pip install -e .
	pip install -e ".[dev]"
	@echo "Installing Playwright browsers..."
	python -m playwright install chromium
	@echo "✓ Installation complete"

setup: install ## Setup project (alias for install)
	@echo "Setting up environment file..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env from .env.example"; fi
	@echo "✓ Setup complete"

run-osc-login: ## Run OSC login and quote creation script
	@echo "Running OSC automation workflow..."
	python scripts/osc/login_and_create_quote.py

run-osc-main: ## Run OSC main automation script  
	@echo "Running OSC main automation script..."
	python scripts/osc/main.py

run-osc-main: ## Run main OSC automation workflow
	@echo "Running main OSC automation workflow..."
	python scripts/osc/main.py

fmt: ## Format code with ruff
	@echo "Formatting code..."
	ruff format .
	ruff check --fix .
	@echo "✓ Formatting complete"

lint: ## Lint code with ruff
	@echo "Running linter..."
	ruff check .

typecheck: ## Type check with mypy
	@echo "Running type checker..."
	mypy core/ apps/

clean: ## Clean generated files
	@echo "Cleaning generated files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf dist/ build/ downloads/ traces/
	find apps/*/logs -name "*.log" -delete 2>/dev/null || true
	find apps/*/reports -name "*.png" -delete 2>/dev/null || true
	@echo "✓ Cleanup complete"
