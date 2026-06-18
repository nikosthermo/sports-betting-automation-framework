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

Hosted Allure report:

```text
https://nikosthermo.github.io/sports-betting-automation-framework/
```

## Repository Structure

```text
sports-betting-automation-framework/
├── .github/workflows/ci.yml
├── docs/
│   ├── test-plan.md
│   ├── execution-results-and-bugs.md
│   └── strategy-and-recommendations.md
├── evidence/screenshots/
│   ├── bug-001-negative-balance.png
│   ├── bug-002-potential-payout-hardcoded-as-stake-x2.png
│   ├── bug-003-balance-does-not-refresh-after-bet-placement.png
│   ├── bug-004-bet-placement-response-currency-usd.png
│   ├── bug-005-bet-receipt-match-order.png
│   └── bug-006-upcoming-shows-past-events.png
├── src/sports_betting/
│   ├── config.py
│   ├── api/
│   │   ├── clients/
│   │   └── services/
│   └── ui/
│       ├── pages/
│       └── services/
├── tests/
│   ├── conftest.py
│   ├── system_tests/single_bet_placement/
│   └── e2e_tests/single_bet_placement/
├── AGENTS.md
├── Makefile
├── pyproject.toml
└── pytest.ini
```

## Architecture

The framework separates transport, business workflows, page objects, and tests:

- API clients handle raw HTTP calls.
- API services expose business-oriented setup and assertions.
- UI page objects wrap Selenium locators and interactions.
- UI services compose page objects into user journeys.
- Tests stay short and scenario-focused.

This keeps the assignment small while demonstrating how the framework could scale without turning every test into Selenium plumbing.

## Test Organization

The test tree is organized by test layer first, then feature domain:

- `tests/system_tests/single_bet_placement` contains API/business-rule checks that validate server-side behavior directly.
- `tests/e2e_tests/single_bet_placement` contains browser-level user journeys that validate the integrated UI flow.

Pytest markers preserve technical filtering:

- `@pytest.mark.api` for API/system tests.
- `@pytest.mark.e2e` for browser E2E tests.

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

For local demos, you can also create an uncommitted `.env` file:

```bash
SPORTY_BASE_URL=<assignment-app-url>
SPORTY_USER_ID=<assignment-user-id>
SPORTY_HEADLESS=true
SPORTY_TIMEOUT_SECONDS=12
```

The framework loads `.env` automatically when present, but exported environment variables take priority.

Optional variables:

```bash
export SPORTY_HEADLESS="true"
export SPORTY_TIMEOUT_SECONDS="12"
```

For this assignment, use the values provided in the assignment instructions for `SPORTY_BASE_URL` and `SPORTY_USER_ID`.

## Running Tests

Run all tests:

```bash
python -m pytest
```

This includes the live browser E2E test, which currently exposes documented product defects.

Run API tests only:

```bash
make test-api
```

Run UI E2E tests only:

```bash
make test-e2e
```

If `SPORTY_BASE_URL` or `SPORTY_USER_ID` is not set, authenticated tests skip with a clear message.

## Allure Reporting

Test commands write Allure result files to `allure-results/`.

Install the Allure command-line tool locally to view HTML reports.

macOS:

```bash
brew install allure
```

Linux:

```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt update
sudo apt install allure
```

Windows:

```powershell
scoop install allure
```

Cross-platform npm alternative:

```bash
npm install -g allure-commandline
```

Verify the installation:

```bash
allure --version
```

Generate API test results:

```bash
make test-api
```

Generate E2E test results:

```bash
make test-e2e
```

Open the interactive report:

```bash
make report-open
```

`allure-pytest` is installed with the development dependencies. The Allure command-line tool is only needed for opening or generating the HTML report locally.

## Quality Gates

Install the development toolchain:

```bash
make install-dev
```

Run all local quality gates:

```bash
make quality
```

This runs:

- Ruff linting, including import sorting checks.
- Ruff formatting checks.
- Google-style docstring convention checks through Ruff's pydocstyle rules.
- Credential leak scanning with `detect-secrets`.
- API Pytest checks with Allure result generation.

Install commit-time hooks:

```bash
pre-commit install
```

Run hooks against the full repository:

```bash
pre-commit run --all-files
```

The secret scanner uses `.secrets.baseline`. If a new intentional false positive appears, audit it before updating the baseline.

The browser E2E is intentionally kept outside `make quality` because it exercises the live application and currently exposes the documented receipt match-order defect. Run it explicitly with:

```bash
make test-e2e
```

## Known E2E Product Defects

The current UI E2E test is expected to fail against the live application because it exposes documented product defects in the critical bet placement journey.

Current examples:

```text
receipt match: expected 'Manchester Utd vs Chelsea', got 'Chelsea vs Manchester Utd'
receipt payout: expected '€24.50', got '€20.00'
header balance after placement: expected to contain '€110.00', got 'Balance: €120.00'
```

These are documented in `docs/execution-results-and-bugs.md` as `BUG-002`, `BUG-003`, and `BUG-005`. The most critical documented defect is `BUG-001`, where repeated placement without refresh can drive the user's balance negative.

## GitHub Actions CI

The repository includes a CI workflow at `.github/workflows/ci.yml`.

Configure these repository settings before running CI:

1. Add repository variable `SPORTY_BASE_URL`.
2. Add repository secret `SPORTY_USER_ID`.
3. Enable GitHub Pages with source set to `GitHub Actions`.

The workflow runs on pushes to `main`, pull requests targeting `main`, and manual dispatch.

CI steps:

- Checks out the repository.
- Sets up Python 3.11.
- Installs the project with development dependencies.
- Loads runtime configuration from GitHub repository variables and secrets.
- Verifies Chrome is available.
- Runs Ruff linting, formatting checks, Google-style docstring checks, and credential scanning.
- Runs API tests.
- Runs UI E2E tests in headless Chrome.
- Generates Allure raw results and an HTML report.
- Uploads Allure artifacts to the workflow run.
- Publishes the Allure HTML report to GitHub Pages for `main` branch runs.

The UI E2E step is allowed to complete report generation even when it finds the documented product defect. The workflow marks the run failed after publishing artifacts so reviewers can inspect the Allure report.

For documentation-only commits where you intentionally do not want to run the live test pipeline, include a standard skip token in the commit message:

```bash
git commit -m "docs: refine QA documentation [skip ci]"
```

## Tooling Choices

- `pytest` for concise fixtures, markers, and readable assertions.
- `requests` for direct API validation.
- `selenium` for required browser automation against Chrome.
- `allure-pytest` for structured test reporting and UI failure attachments.
- `pyproject.toml` for modern Python packaging and editable installs.
- `ruff` for linting, import sorting, formatting checks, and Google-style docstring enforcement.
- `detect-secrets` for credential leak prevention.
- `pre-commit` for local commit-time quality gates.

## Known Specification Ambiguity

The assignment text contains conflicting minimum stake references:

- Business rules: stake minimum is `€1.00`.
- Validation table: minimum is `€1.01`.
- UI expected copy: `Minimum stake is €1.00`.
- OpenAPI schema defines minimum as `1`.

The current automated tests avoid relying on this ambiguous boundary. Before adding automated minimum-stake boundary coverage, this should be clarified with the product owner.
