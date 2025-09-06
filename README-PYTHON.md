# Budget Tracker CLI - Python Version

A barebones Python CLI setup for you to learn and build upon! 🐍

## What's Been Set Up For You

### Project Structure
```
Budget-Tracker/
├── legacy-backup/          # Your original TypeScript code
├── src/
│   └── budget_tracker/
│       ├── __init__.py
│       ├── cli.py          # Main CLI entry point (basic setup)
│       ├── commands/       # Command implementations (placeholders)
│       │   ├── __init__.py
│       │   ├── link.py
│       │   ├── exchange.py
│       │   └── pull.py
│       ├── services/       # API services (placeholders)
│       │   ├── __init__.py
│       │   └── plaid_client.py
│       └── utils/          # Utilities (placeholders)
│           ├── __init__.py
│           └── storage.py
├── pyproject.toml          # Modern Python packaging config
├── .env.example            # Environment variables template
└── README-PYTHON.md       # This file
```

## Getting Started

### 1. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install basic dependencies
pip install -e .
```

### 2. Test the Basic CLI
```bash
# Test the hello command
budget-tracker hello

# See all available commands
budget-tracker --help

# Test placeholder commands
budget-tracker link
budget-tracker pull --month 2024-01 --format csv
```

### 3. Your Learning Journey

The CLI is set up with **Typer** - a modern Python CLI framework. All the command placeholders are ready for you to implement:

1. **Start with `cli.py`** - This is your main entry point
2. **Implement `services/plaid_client.py`** - Add Plaid API integration
3. **Build `utils/storage.py`** - Handle token storage
4. **Fill in the commands** - `link.py`, `exchange.py`, `pull.py`

### 4. When You're Ready for More Dependencies

The `pyproject.toml` includes optional dependencies you can install as needed:

```bash
# Add Plaid support
pip install -e ".[plaid]"

# Add data validation
pip install -e ".[validation]"

# Add HTTP client
pip install -e ".[http]"

# Add development tools
pip install -e ".[dev]"
```

### 5. Development Tools (Optional)

When you install the dev dependencies, you get:
- **Black**: Code formatter (`black .`)
- **isort**: Import sorter (`isort .`)
- **mypy**: Type checker (`mypy src/`)
- **pytest**: Testing framework (`pytest`)

## Learning Resources

- **Typer Documentation**: https://typer.tiangolo.com/
- **Plaid Python SDK**: https://github.com/plaid/plaid-python
- **Python Packaging**: https://packaging.python.org/

## Your Original Code

Your TypeScript implementation is safely stored in `legacy-backup/` for reference!

Happy coding! 🚀
