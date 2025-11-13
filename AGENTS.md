# Repository Guidelines

## Project Structure & Module Organization
This FastAPI backend keeps nearly all HTTP logic inside `main.py`, including the `FastAPI` `app`, validation helpers, and the in-memory `db` seeded for login flows. Tests live in `test/`, with `test_login.py` covering the `/login` workflow through `TestClient`. Dependency manifests are split between `requirements.txt` for runtime and `requirements-dev.txt` (which extends it) for pytest/httpx tooling. Shared pytest configuration is centralized in `pytest.ini`, so add new suites under `test/` with filenames following `test_*.py`.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate`: create an isolated interpreter that matches the Python 3.10 target.
- `pip install -r requirements-dev.txt`: install FastAPI, Pydantic, Uvicorn, pytest, and the test client stack in one step.
- `uvicorn main:app --reload`: run the development API server from the repo root; reload keeps validators in sync while editing.
- `pytest`: executes the full suite with `-v --tb=short` flags inherited from `pytest.ini`.
- `pytest test/test_login.py -k success`: target a single scenario when iterating on specific branches.

## Coding Style & Naming Conventions
Use 4-space indentation, keep functions and variables in `snake_case`, and reserve `PascalCase` for Pydantic models (`UserData`) and pytest classes (`TestLoginAPI`). Type hints are mandatory for public helpers (see `search_user_by_email`). Validation helpers should raise FastAPI/Pydantic errors with localized messages. When adding models, extend the existing `Field(..., description=...)` pattern and keep regex constants uppercase.

## Testing Guidelines
Pytest with `fastapi.testclient.TestClient` drives contract tests; new endpoints need at least one success and one failure path that mirrors the fixtures in `test_login.py`. Obey the discovery rules in `pytest.ini` (`test_*.py`, `Test*` classes, `test_*` functions) to keep CI happy. Prefer parametrization for format matrices and patching (`unittest.mock.patch`) when isolating authentication. Run `pytest --maxfail=1` before pushing to ensure the suite stays deterministic.

## Commit & Pull Request Guidelines
Commits in `.git/logs/HEAD` show Conventional Commit prefixes (`feat: add httpexcption to http exception`), so continue using short, imperative summaries with a clear scope. Group unrelated work into separate commits to keep review tight. Every PR should include: context on the API or validator touched, the manual/automated tests executed, and references to issues or product tickets. Attach new request/response samples or screenshots whenever an endpoint contract changes, and avoid merging without at least one reviewer sign-off.
