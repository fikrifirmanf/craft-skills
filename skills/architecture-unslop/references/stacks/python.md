# Python

**Detect:** `pyproject.toml`, `requirements*.txt`, `setup.cfg`, `Pipfile`. Target Python 3.11+ with type hints.

## Spelling the layout
- Package root `app/` (or the project name) under `src/` or at the top level, with `__init__.py` in every package.
- `app/modules/orders/{domain,application,adapters/inbound,adapters/outbound}/`. Python avoids `in` as a package name because `in` is a keyword, so use `inbound`/`outbound`.
- A module's public entry is `app/modules/<context>/__init__.py` (or `api.py`).
- Composition root: `app/main.py`.
- snake_case modules and functions, PascalCase classes.

## Slice idioms
| Piece | Idiom |
|---|---|
| Id | `OrderId = NewType('OrderId', UUID)` |
| Value object | `@dataclass(frozen=True, slots=True) class Money` with `__post_init__` validation; `cents: int`, never `float` |
| Aggregate | Regular class with leading-underscore state, `@classmethod draft()` / `restore()`, properties without setters |
| Domain error | `class DomainError(Exception)` with a `code: str` attribute |
| Port | `typing.Protocol` (`class OrderRepository(Protocol)`) |
| Use case | Class with injected ports and `async def execute(self, command)` (or sync, matching the project) |
| Inbound validation | Pydantic model with `model_config = ConfigDict(extra='forbid')` in the inbound adapter only. Never in the domain |
| Database | `psycopg` 3 or `asyncpg` with `%s`/`$1` parameters; `executemany` or `unnest` for child rows; connection timeouts set in `main.py` |
| Tests | `pytest`; domain tests import only `app.modules.orders.domain` |

Use relative imports inside a module (`from .money import Money`) and the public entry across modules (`from app.modules.billing import charge`).

## Install commands to report
```bash
pip install "psycopg[binary]" pydantic
pip install pytest   # or: uv add --dev pytest
```
Add `fastapi`, `flask` or `django` only if named. Its code lives in `adapters/inbound` and `main.py`. With Django, keep Django models in `adapters/outbound/django_models.py` and map them to domain objects.

## Extra boundary tooling
`import-linter` with `layers` and `independence` contracts enforces the same rules in CI.
