# Strategy and Recommendations

## Why These Two Tests Were Automated

The UI E2E test automates the critical revenue journey: select odds, enter stake, place a bet, and validate receipt data. It covers integration between match data, bet slip calculation, placement, and final user-facing confirmation.

The API test automates stake precision validation because financial inputs must be enforced below the UI. API validation gives fast, stable feedback and protects against client-side bypasses.

## Intentionally Left Manual

Error modal retry behavior is left manual initially because deterministic server failure triggering is not exposed in the public contract. Automating it without a controllable failure hook would likely be flaky or artificial.

Date and odds filter exploration is left manual in this scoped submission because it has lower financial risk than placement and payout correctness. It is still covered in the manual test plan because filter defects can hide or misrepresent available matches.

Visual polish, copy quality, and exploratory wallet behavior remain manual because the assignment rewards focused, risk-based coverage over broad low-signal automation.

## Recommendations for Scale

1. Add CI with separate API and UI jobs. API tests should run on every pull request; UI tests can run in Chrome headless with screenshots and browser logs captured on failure.
2. Introduce deterministic test data controls. A QA-only endpoint or seed mechanism should create known matches, odds, balances, and controllable success/failure responses.
3. Clarify the specification. Resolve the minimum stake conflict between `€1.00` and `€1.01`, define receipt match ordering explicitly, and require the receipt to use backend-confirmed odds/payout values.

## Agentic QA Opportunities

AI agents can help maintain this suite by comparing OpenAPI changes against test coverage, proposing risk-based new scenarios, summarizing failed CI evidence, and generating focused exploratory charters. Human review should remain mandatory for business-risk prioritization and financial correctness decisions.
