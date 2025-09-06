.PHONY: setup run clean

VENV := venv
VENV_BIN := $(VENV)/bin

setup: ## Create virtual environment and install
	python3 -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install --force-reinstall -e .

run: ## Run the CLI with any arguments
	$(VENV_BIN)/budget-tracker $(filter-out $@,$(MAKECMDGOALS))

hello: ## Test the hello command
	$(VENV_BIN)/budget-tracker hello

clean: ## Remove virtual environment
	rm -rf $(VENV)

# Catch-all target to prevent Make from complaining about unknown targets
%:
	@:
