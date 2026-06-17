# Agent Operating Notes

This repository is a scoped QA automation submission for a sports betting single-bet flow. It is designed so AI agents and human contributors can make focused changes without weakening the assignment narrative, test reliability, or evidence trail.

## Scope

- Keep the project focused on Single Bet Placement unless the user explicitly asks to expand scope.
- Favor high-risk betting behavior over broad low-signal coverage.
- Do not add tooling, abstractions, or test layers unless they improve maintainability, reporting, reliability, or risk coverage.
- Preserve the distinction between assignment deliverables:
  - `docs/test-plan.md`
  - `docs/execution-results-and-bugs.md`
  - `docs/strategy-and-recommendations.md`
  - automation under `src/` and `tests/`

## Architecture Map

- `src/sports_betting/config.py` loads runtime configuration from environment variables and optional local `.env`.
- `src/sports_betting/api/clients` contains transport-level HTTP code only.
- `src/sports_betting/api/services` contains business-oriented API workflows and setup helpers.
- `src/sports_betting/ui/pages` contains Selenium page objects and locators.
- `src/sports_betting/ui/services` contains user-level workflows composed from page objects.
- `tests/system_tests/single_bet_placement` contains API/business-rule tests.
- `tests/e2e_tests/single_bet_placement` contains browser user-journey tests.
- `evidence/screenshots/bug-*.png` contains curated manual evidence only.
- `allure-results/` and `allure-report/` are generated artifacts and must not be committed.

## Patterns to Follow

- Keep tests feature-oriented. Add new tests under a feature folder such as `single_bet_placement`, not under generic `api` or `ui` folders.
- Use pytest markers to express execution type:
  - `@pytest.mark.api`
  - `@pytest.mark.e2e`
- Use API services for setup and state reads instead of duplicating raw HTTP calls in tests.
- Use page objects for Selenium locators and direct interactions.
- Use UI services for multi-step browser workflows.
- Add Allure labels and meaningful `allure.step(...)` blocks for new tests.
- Keep test docstrings short and focused on why the test was selected.
- Use backend-confirmed values for financial assertions whenever available.
- Keep manual bug reports ordered by business impact, not discovery order.

## Anti-Patterns to Avoid

- Do not hardcode `SPORTY_BASE_URL`, `SPORTY_USER_ID`, or any real credential in source, docs, or tests.
- Do not commit `.env`, browser profiles, Allure output, caches, or uncurated screenshots.
- Do not put business workflows directly inside page objects.
- Do not put Selenium locators directly inside tests unless there is a strong reason.
- Do not use sleeps for synchronization; prefer explicit waits.
- Do not rely on test execution order.
- Do not make live E2E tests part of `make quality` while the documented product defect is expected to fail.
- Do not merge distinct defects only because they occur in the same flow; keep different root causes and owners separate.

## Test Data and Configuration

- Use `SPORTY_BASE_URL` for the target app URL.
- Use `SPORTY_USER_ID` for authenticated app/API access.
- Local `.env` is allowed for demos, but exported environment variables take priority.
- Use a unique user id per tester or CI run when possible.
- Reset balance before tests that mutate wallet state.
- Treat balance and bet placement as stateful; avoid hidden dependencies between tests.

## Evidence Rules

- Curated screenshots should be named by bug id, for example `bug-001-negative-balance.png`.
- Generated screenshots from failed E2E runs are ignored unless intentionally renamed to `bug-*.png`.
- If a bug report references evidence, make sure the path exists.
- Keep evidence concise; prefer one clear screenshot per high-impact bug.

## Quality Gates

Run before publishing changes:

```bash
make quality
pre-commit run --all-files
```

`make quality` runs linting, formatting checks, credential scanning, and API tests with Allure result generation.

Run the live browser E2E separately:

```bash
make test-e2e
```

The E2E currently exposes a documented product defect, so a failure can be expected unless the application has been fixed.

## CI and Reporting

- GitHub Actions workflow lives at `.github/workflows/ci.yml`.
- CI expects:
  - repository variable `SPORTY_BASE_URL`
  - repository secret `SPORTY_USER_ID`
  - GitHub Pages source set to `GitHub Actions`
- CI publishes Allure HTML reports to GitHub Pages for `main` branch runs.
- The UI E2E step uses `continue-on-error` so report generation still happens before the workflow is marked failed.

## Documentation Rules

- Keep README aligned with the actual repository structure and commands.
- Keep Part A manual docs focused on risk, reproduction clarity, expected vs actual, business impact, and evidence.
- Keep Part C recommendations forward-looking. Do not recommend CI, Allure, or quality gates as future work now that they already exist.
- When adding external context, cite stable public sources and avoid overstating assumptions.
