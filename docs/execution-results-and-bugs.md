# Execution Results and Bugs

Execution date: 2026-06-16

Environment:

- App: value supplied through `SPORTY_BASE_URL`
- Browser target: Latest desktop Chrome
- API docs inspected: `/api/docs?format=json`

Runtime configuration was supplied through `SPORTY_BASE_URL` and `SPORTY_USER_ID`.

## Top Scenario Execution Status

| Scenario | Status | Notes |
| --- | --- | --- |
| SBP-001 Valid single bet | Failed | Automated UI E2E test found receipt match ordering defect. |
| SBP-002 Invalid stake precision | Passed | Automated API test returned `422 invalid_stake_precision`. |
| SBP-003 Insufficient balance | Manual follow-up | Recommended for exploratory execution with valid user id. |

## BUG-001: Success Receipt Displays Match Teams in Reversed Order

Severity: High

Reproduction Steps:

1. Open the app with a valid `user-id`.
2. Select HOME odds for a match where the match list shows `Home Team vs Away Team`.
3. Enter a valid stake.
4. Place the bet.
5. Compare the success receipt match text with the original match card.

Expected Result:

- Receipt preserves match ordering as `homeTeam vs awayTeam`.

Actual Result:

- Automated UI E2E showed receipt text `Chelsea vs Manchester Utd` for API/list match order `Manchester Utd vs Chelsea`.

Business Impact:

- The receipt can misrepresent the selected event, reducing user trust and creating support/reconciliation risk.

Evidence:

- Screenshot: `evidence/screenshots/bug-001-receipt-match-order.png`
- Pytest assertion: expected `Manchester Utd vs Chelsea`, actual `Chelsea vs Manchester Utd`.

## BUG-002: Success Receipt Potential Payout Appears Hardcoded to Stake x 2

Severity: Critical

Reproduction Steps:

1. Open the app with a valid `user-id`.
2. Select an odds button where odds are not exactly `2.00`.
3. Enter stake `10.00`.
4. Note the bet slip potential payout.
5. Place the bet.
6. Compare receipt payout with the bet slip payout and API payout.

Expected Result:

- Receipt payout equals `stake * odds at placement`.

Actual Result:

- Frontend bundle inspection indicates receipt construction uses `stake * 2`.

Business Impact:

- Incorrect payout display is a direct financial correctness defect and can mislead users after bet placement.

Evidence:

- Frontend asset inspection found receipt `potentialPayout` composed as `stake * 2` instead of API response payout or selected odds.

## BUG-003: Reset Balance API Documentation Warns Response May Differ from Persisted Balance

Severity: High

Reproduction Steps:

1. POST `/api/reset-balance` with a valid `x-user-id`.
2. Immediately GET `/api/balance` with the same user id.
3. Compare response body balance from reset with persisted balance.

Expected Result:

- Reset response body and persisted balance are consistent.

Actual Result:

- `POST /api/reset-balance` returned `{"balance":125.5,"currency":"EUR"}`.
- Immediate `GET /api/balance` returned `{"balance":120,"currency":"EUR"}`.

Business Impact:

- Test setup and user wallet recovery flows can become unreliable if API responses do not reflect persisted state.

Evidence:

- Direct API verification on 2026-06-16.
- OpenAPI description also warns: `Balance reset successfully (response payload may differ from persisted balance)`.
