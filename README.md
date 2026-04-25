# devin-test-multiagent

A small "marketplace" backend split across four loosely-coupled services. Each
service owns a different concern and is maintained by a different team
internally, so they tend to have very different failure modes.

```
services/
  auth/           — sessions, tokens, password hashing
  orders/         — inventory + paginated listing
  notifications/  — templated emails, retry/backoff
  gateway/        — request routing across the other three services
```

Each service has its own test module under `tests/`, plus an
`tests/test_integration.py` that exercises a few cross-service flows.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate    # .venv\Scripts\activate on Windows
pip install -e .
pip install -r requirements-dev.txt
pytest
```

## Status

The full suite is currently red. Failures are spread across all four services
— the auth team, orders team, and notifications team have each filed
independent bug reports recently and nobody has had time to triage. The
gateway is also misrouting one prefix. See the failing tests for specifics.
