# Agent Operating Notes

This repository is structured so AI agents and human contributors can work safely on the same QA automation project.

## Scope

- Keep automation focused on the Single Bet Placement feature.
- Prefer small, intention-revealing helpers over broad framework abstractions.
- Do not commit local credentials, real user identifiers, browser profiles, or generated screenshots unless they are intentionally curated evidence.

## Architecture Guidelines

- `src/sports_betting/api/clients` contains transport-level HTTP code.
- `src/sports_betting/api/services` contains business-oriented API workflows.
- `src/sports_betting/ui/pages` contains Selenium page objects.
- `src/sports_betting/ui/services` contains E2E user workflows composed from page objects.
- `tests/system_tests` validates API/business rules directly.
- `tests/e2e_tests` validates browser-level user journeys.

## Test Data

- Use a unique `SPORTY_USER_ID` per tester or CI run.
- Reset balance before tests that mutate balance.
- Avoid test order dependencies.

## Verification

Run before publishing changes:

```bash
python -m pytest
```
