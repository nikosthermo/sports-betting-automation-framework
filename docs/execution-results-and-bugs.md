# Execution Results and Bugs

Execution date: 2026-06-17

Environment:

- App: value supplied through `SPORTY_BASE_URL`
- User context: value supplied through `SPORTY_USER_ID`
- Browser target: Latest desktop Chrome
- API docs inspected: `/api/docs?format=json`
- Test type: Manual execution, exploratory testing, API inspection, and supporting automated evidence where available

## Top Scenario Execution Status

| Scenario | Priority | Status | Highest-impact findings |
| --- | --- | --- | --- |
| SBP-002 Enforce balance across repeated and concurrent bet placement | Critical | Failed | BUG-001, BUG-003 |
| SBP-001 Place a valid single bet and verify confirmation data | Critical | Failed | BUG-002, BUG-003, BUG-004, BUG-005 |
| SBP-003 Default match list shows upcoming pre-match events only | High | Failed | BUG-006 |

The defects below are ordered by business criticality, not by discovery order. The highest-risk findings are listed first because they can directly affect financial exposure, payout correctness, and customer trust.

## Exploratory Notes

- Compared UI receipt values with the `/api/place-bet` response.
- Repeated placement without page refresh to observe balance behavior.
- Inspected the default event list and date ordering on the `Upcoming Football Matches` page.
- Checked whether the issues were backend-generated or introduced by frontend rendering/state logic.

External context used for the event-list risk: odds products distinguish pre-match/upcoming odds from historical results. For example, The Odds API describes its feed as covering in-play and upcoming events, while OddsPortal presents historical odds/results in a separate archive-style results area. This supports treating past events in the primary upcoming betting list as a product/UX risk rather than a preferred default.

Sources:

- https://the-odds-api.com/
- https://www.oddsportal.com/results/

## BUG-001: Backend Allows Negative Balance Through Repeated Placement Without Refresh

Severity: Critical

Reproduction Steps:

1. Open the app with a valid `user-id`.
2. Place one or more valid bets until the persisted balance is low or zero.
3. Do not refresh the page.
4. Continue placing bets using the stale displayed balance, or submit repeated/concurrent placement attempts.
5. Inspect persisted balance through UI refresh or API.

Expected Result:

- Backend validates stake against the actual persisted user balance on every placement request.
- A bet that exceeds available balance is rejected with an insufficient balance error.
- Balance never becomes negative.
- Concurrent placement is controlled with locking/idempotency or `409 bet already in progress`.

Actual Result:

- UI validation is based on stale frontend balance state.
- Backend allows additional bets and persisted balance can become negative.

Business Impact:

- This is a direct financial exposure. Users can place multiple bets without sufficient funds, resulting in negative balances and potential revenue loss.

Evidence:

- Screenshot: `evidence/screenshots/bug-001-negative-balance.png`
- Manual exploratory testing showed repeated placement without refresh can drive balance below zero.

## BUG-002: Receipt Potential Payout Is Hardcoded as Stake x 2

Severity: Critical

Reproduction Steps:

1. Open the app with a valid `user-id`.
2. Select HOME odds for `Manchester Utd vs Chelsea`.
3. Enter stake `10.00`.
4. Place the bet.
5. Compare receipt payout with the selected odds and `/api/place-bet` response.

Expected Result:

- Payout equals `stake * odds`.
- For stake `10.00` and odds `2.45`, payout should be `24.50`.
- Receipt should display the backend-confirmed payout.

Actual Result:

- Backend response returns the correct payout:

```json
{
  "message": "Bet placed successfully",
  "matchId": "premier-league-manutd-chelsea",
  "selection": "HOME",
  "stake": 10,
  "odds": 2.45,
  "payout": 24.5,
  "balance": 50,
  "currency": "USD"
}
```

- UI receipt displays payout as if calculated by `stake * 2`.
- This indicates the receipt is using frontend hardcoded calculation instead of backend-confirmed payout.
- This may be related to the broader monetary consistency issue in `BUG-004`; however, no currency conversion requirement exists in the specification, no additional FX/rate API call was observed, and the displayed value matches a hardcoded multiplier pattern rather than a USD/EUR conversion.

Business Impact:

- Incorrect payout display is a financial correctness issue. It can mislead users about potential returns and create high-risk disputes if UI and backend records disagree.

Evidence:

- Manual API inspection showed backend payout `24.5` for `10 * 2.45`.
- UI receipt showed a payout consistent with `10 * 2`.
- Screenshot: `evidence/screenshots/bug-002-potential-payout-hardcoded-as-stake-x2.png`

## BUG-003: Balance Does Not Refresh After Successful Bet Placement

Severity: High

Reproduction Steps:

1. Open the app with a valid `user-id`.
2. Note the displayed balance in the header and bet slip.
3. Place a valid bet.
4. Close the success receipt.
5. Observe the header and bet slip balance without refreshing the page.
6. Refresh the page and compare the balance again.

Expected Result:

- Balance refreshes immediately after a successful bet.
- Header and bet slip display the same updated balance.
- User does not need a manual browser refresh to see available funds.

Actual Result:

- Balance remains stale after bet placement.
- User must refresh the page manually to see the updated balance.

Business Impact:

- Stale balance misleads the user and contributes to overspending risk. It also masks backend state changes and creates conditions for repeated bets against an outdated displayed balance.

Evidence:

- Screenshot: `evidence/screenshots/bug-003-balance-does-not-refresh-after-bet-placement.png`
- Behavior confirmed by manual placement and page refresh comparison.

## BUG-004: Bet Placement API Returns USD Currency for EUR Product

Severity: High

Reproduction Steps:

1. Open the app with a valid `user-id`.
2. Place a valid bet.
3. Inspect the `/api/place-bet` response.
4. Compare response currency with the feature specification and UI currency.

Expected Result:

- API response currency is `EUR`.
- UI and backend currency are consistent.

Actual Result:

- API response returns `"currency": "USD"`.
- UI displays EUR symbols, likely hardcoded in the frontend.

Business Impact:

- Currency inconsistency is a financial correctness and compliance risk. It can cause inaccurate receipts, accounting issues, and customer confusion about the currency being wagered.

Evidence:

- Screenshot: `evidence/screenshots/bug-004-bet-placement-response-currency-usd.png`

```json
{
  "message": "Bet placed successfully",
  "matchId": "premier-league-manutd-chelsea",
  "selection": "HOME",
  "stake": 10,
  "odds": 2.45,
  "payout": 24.5,
  "balance": 50,
  "currency": "USD"
}
```

## BUG-005: Bet Receipt Displays Match Teams in Reversed Order

Severity: High

Reproduction Steps:

1. Open the app with a valid `user-id`.
2. Select HOME odds for `Manchester Utd vs Chelsea`.
3. Enter stake `10.00`.
4. Place the bet.
5. Compare the success receipt match text with the match list and API match data.

Expected Result:

- Receipt preserves the source event order: `homeTeam vs awayTeam`.
- For this match, receipt should show `Manchester Utd vs Chelsea`.

Actual Result:

- Receipt shows `Chelsea vs Manchester Utd`.
- API/match list ordering is correct, so the defect appears to be in frontend receipt rendering.

Business Impact:

- Users may believe they placed a bet on the wrong event or side, causing loss of trust, support contacts, and potential dispute/reconciliation risk.

Evidence:

- Screenshot: `evidence/screenshots/bug-005-bet-receipt-match-order.png`
- Automated assertion also reproduced the issue: expected `Manchester Utd vs Chelsea`, actual `Chelsea vs Manchester Utd`.

## BUG-006: Upcoming Matches Page Shows Past Events by Default

Severity: Medium

Reproduction Steps:

1. Open the app with a valid `user-id`.
2. Land on the `Upcoming Football Matches` page.
3. Observe the first visible events and kickoff dates.
4. Compare the default list with the feature scope: upcoming football pre-match events only.

Expected Result:

- Default view shows upcoming/pre-match events only.
- Past events are hidden from the primary betting flow or separated into a clearly labeled past-results/archive area.
- If date filtering is frontend-owned, default filter state should start at the current date or otherwise exclude past events.

Actual Result:

- Default page shows all events, with past events appearing first.
- Filtering appears to be handled on the frontend rather than preventing past events from being shown by default.

Business Impact:

- Users are presented with irrelevant or unavailable betting opportunities before valid upcoming markets. This increases confusion and can reduce conversion in the core betting flow.

Evidence:

- Screenshot: `evidence/screenshots/bug-006-upcoming-shows-past-events.png`
- UI logic inspection indicates the event filtering is handled on the frontend.
