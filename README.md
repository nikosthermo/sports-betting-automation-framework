# Sports Betting Automation Framework

Scoped QA submission for Sporty's Single Bet Placement assignment.

The repository combines manual QA deliverables with a small Python automation framework using Selenium WebDriver, `requests`, Chrome, and Pytest.

## What Is Included

- `docs/test-plan.md` - prioritized manual test scenarios.
- `docs/execution-results-and-bugs.md` - execution notes and defect reports.
- `docs/strategy-and-recommendations.md` - automation rationale and scaling recommendations.
- `src/sports_betting` - reusable API and UI automation code.
- `tests/system_tests/single_bet_placement` - direct API/business-rule tests for the feature.
- `tests/e2e_tests/single_bet_placement` - browser E2E tests for the feature.

## Architecture

The framework separates transport, business workflows, page objects, and tests:

- API clients handle raw HTTP calls.
- API services expose business-oriented setup and assertions.
- UI page objects wrap Selenium locators and interactions.
- UI services compose page objects into user journeys.
- Tests stay short and scenario-focused.

This keeps the assignment small while demonstrating how the framework could scale without turning every test into Selenium plumbing.

## Requirements

- Python 3.11+
- Latest desktop Chrome
- ChromeDriver available through Selenium Manager

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Configuration

The framework intentionally does not hardcode the application URL or user id. Pass both values through environment variables before running tests.

```bash
export SPORTY_BASE_URL="<assignment-app-url>"
export SPORTY_USER_ID="<assignment-user-id>"
```

Optional variables:

```bash
export SPORTY_HEADLESS="true"
export SPORTY_TIMEOUT_SECONDS="12"
```

For this assignment, use the values provided in the assignment instructions for `SPORTY_BASE_URL` and `SPORTY_USER_ID`.

## Running Tests

Run everything:

```bash
python -m pytest
```

Run API tests only:

```bash
python -m pytest tests/system_tests/single_bet_placement -m api
```

Run UI E2E tests only:

```bash
python -m pytest tests/e2e_tests/single_bet_placement -m e2e
```

If `SPORTY_BASE_URL` or `SPORTY_USER_ID` is not set, authenticated tests skip with a clear message.

## Tooling Choices

- `pytest` for concise fixtures, markers, and readable assertions.
- `requests` for direct API validation.
- `selenium` for required browser automation against Chrome.
- `pyproject.toml` for modern Python packaging and editable installs.
- Optional `ruff` configuration is included for local linting, but it is not required to execute tests.

## Known Specification Ambiguity

The assignment text contains conflicting minimum stake references:

- Business rules: stake minimum is `€1.00`.
- Validation table: minimum is `€1.01`.
- UI expected copy: `Minimum stake is €1.00`.

The automation currently follows the API documentation and observed frontend copy around `€1.00`; this should be clarified with the product owner before expanding coverage.
