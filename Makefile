.PHONY: setup run clean

VENV := venv
VENV_BIN := $(VENV)/bin

setup: ## Create virtual environment and install
	python3 -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -e .

run: ## Show CLI help
	$(VENV_BIN)/budget-tracker --help

hello: ## Test the hello command
	$(VENV_BIN)/budget-tracker hello

clean: ## Remove virtual environment
	rm -rf $(VENV)
