# Budget Tracker

Budget tracking tool built with Plaid API. Migrating from a CLI app (`budget_tracker`) to a web app (`budget_tracker_api`) powered by FastAPI + React.

## Project Structure

- `src/budget_tracker/` - Original CLI app (Typer)
- `src/budget_tracker_api/` - New web app
  - `app/` - FastAPI backend (serves static frontend from `app/public/`)
  - `frontend/` - React frontend (Vite)

## Commands

### Install

```sh
poetry install                # install python deps
cd src/budget_tracker_api/frontend && npm install  # install frontend deps
```

### Dev

```sh
poetry run dev                # starts both: Vite build (watch) + FastAPI (uvicorn w/ reload)
```

`dev` auto-installs frontend npm deps if missing, does an initial Vite build, then runs `npm run build:watch` and `uvicorn` in parallel. Backend serves at `http://localhost:8000`.

### Build

```sh
cd src/budget_tracker_api/frontend && npm run build        # build frontend
cd src/budget_tracker_api/frontend && npm run build:watch   # build frontend (watch mode)
```

### CLI (legacy)

```sh
poetry run budget-tracker     # run the CLI app
```

### Lint / Test

```sh
poetry run ruff check .       # lint
poetry run mypy .             # type check
poetry run pytest             # test
```
