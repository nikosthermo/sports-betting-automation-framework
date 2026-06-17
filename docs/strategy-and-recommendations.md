# Strategy and Recommendations

## Why These Two Tests Were Automated

The UI E2E test covers the critical revenue journey: selecting odds, entering a stake, placing a bet, and validating the receipt. It was chosen because this path combines the highest-risk user-facing surfaces: event identity, stake, odds, payout, currency, and post-placement confirmation. The current failure is valuable because it exposes a real receipt-data defect rather than only proving a happy path.

The API test covers stake precision validation directly through `/api/place-bet`. It was chosen because financial validation must be enforced below the UI. A user or client can bypass frontend controls, so API-level validation gives faster and more stable feedback on a core business rule.

These two tests were selected over broader UI coverage because they provide high signal with low maintenance cost: one integrated user journey and one direct backend validation check.

## What Was Intentionally Left Manual

Repeated placement, stale balance, and negative balance behavior were kept manual in this scoped submission because they are exploratory, stateful, and concurrency-sensitive. They should become automated once the application exposes deterministic balance setup and reliable controls for concurrent or duplicate placement.

Error modal retry behavior was left manual because the public contract does not expose a deterministic way to trigger server-side placement failures. Automating it without a controllable failure hook would be brittle.

Date and odds filter behavior was kept mostly manual because it is lower financial risk than bet placement, payout, and balance integrity. It remains in the manual test plan because incorrect filtering can still hide valid markets or show invalid/past markets.

Visual polish, copy review, and layout consistency remain manual because they benefit from human judgment and are not the highest-risk automation target for this scoped assignment.

## Current Engineering Baseline

The project already includes:

- GitHub Actions CI.
- Ruff linting, formatting, import sorting, and Google-style docstring checks.
- `detect-secrets` credential scanning.
- Pre-commit hooks.
- Allure result generation and GitHub Pages-hosted reporting.
- Environment-driven configuration with optional local `.env` loading.

Future recommendations therefore focus on product quality, test data control, deeper test layers, and non-functional risk.

## Top Recommendations for Scale

1. Introduce deterministic test data and state controls.

   Add QA-only setup endpoints or seeded fixtures for known matches, odds, user balances, and placement outcomes. This would make balance, insufficient funds, duplicate placement, and error-modal behavior reliable enough for automation.

2. Add contract and monetary consistency checks.

   Use OpenAPI/schema validation and targeted API assertions for currency, odds, payout, balance deduction, and response/persisted-state consistency. These checks should explicitly verify that UI receipts use backend-confirmed values rather than frontend recalculation.

3. Add concurrency and non-functional test layers.

   Add API-level concurrent placement tests to verify locking, idempotency, and insufficient-balance enforcement under repeated requests. Add lightweight performance/load checks for multiple users placing single bets at the same time, with thresholds for response time, error rate, and balance consistency.

## Additional Functional Increments

- Automate insufficient balance rejection once deterministic balance setup exists.
- Automate receipt validation against the exact `/api/place-bet` response.
- Add tests for selection replacement and `Remove All` behavior.
- Add date and odds filter tests for inclusive boundaries and invalid ranges.
- Add reset-balance consistency checks if the endpoint remains part of the test support contract.

## Security and Risk Recommendations

- Validate that `x-user-id` cannot be used to access or mutate another user's balance or bet state.
- Add authorization tests for missing, malformed, and unknown user contexts.
- Check that stake, match id, and selection fields are validated server-side even when the UI blocks invalid input.
- Add rate-limit or abuse checks around repeated placement attempts.

## Specification Clarifications Needed

- Resolve the minimum stake ambiguity between `€1.00` and `€1.01`.
- Clarify whether `/api/place-bet` response currency must always be `EUR`.
- Define whether receipt values must come from backend response values.
- Define default event-list behavior for past events versus upcoming/pre-match events.
- Define concurrency behavior for repeated placement and duplicate submits.

## Agentic QA Opportunities

AI agents can help maintain this suite by comparing OpenAPI changes against test coverage, proposing risk-based new scenarios, summarizing failed CI and Allure evidence, and generating focused exploratory charters. Human review should remain mandatory for financial correctness, business-risk prioritization, and final defect severity.
