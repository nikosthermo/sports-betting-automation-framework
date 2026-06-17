# Test Plan: Single Bet Placement

## SBP-001: Place a Valid Single Bet and Verify Confirmation Data

Priority: Critical

Risk Rationale: This is the core revenue journey. Any mismatch between selected event, stake, odds, payout, balance, or currency can mislead the customer and create financial reconciliation issues.

Steps:

1. Open the app with a valid `user-id`.
2. Confirm the header and bet slip show the current EUR balance.
3. Select the HOME odds for an upcoming match.
4. Enter stake `10.00`.
5. Confirm the displayed potential payout equals `stake * selected odds`.
6. Place the bet.
7. Compare the success receipt against the selected match, selection, stake, odds, payout, currency, and API response.
8. Close the receipt and confirm the main flow is reset.

Expected Result:

- `Place Bet` enters a loading state and resolves to one final outcome.
- Receipt preserves `homeTeam vs awayTeam` ordering.
- Receipt uses the odds and payout returned by the backend.
- Currency is consistently EUR across UI and API contract.
- Balance is deducted by the stake and is refreshed everywhere it is displayed.
- Closing the receipt clears the active selection and stake.

## SBP-002: Enforce Balance Across Repeated and Concurrent Bet Placement

Priority: Critical

Risk Rationale: Balance enforcement protects the business from users placing bets without available funds. UI-only validation is insufficient because stale UI state, duplicate submits, concurrent requests, or direct API calls can bypass it.

Steps:

1. Reset the user's balance.
2. Place a valid bet that deducts part of the balance.
3. Without refreshing the page, attempt additional bets that cumulatively exceed the remaining balance.
4. Repeat the same risk through direct API calls or rapid placement attempts if possible.
5. Refresh the page and check the persisted balance.

Expected Result:

- Backend rejects any bet that exceeds the user's actual persisted balance.
- User balance never becomes negative.
- UI refreshes balance immediately after each successful bet.
- Duplicate/concurrent placement is blocked or returns a clear error such as `409 bet already in progress`.

## SBP-003: Default Match List Shows Upcoming Pre-Match Events Only

Priority: High

Risk Rationale: The feature scope is upcoming football pre-match betting. Showing past events first can lead users to select unavailable or misleading markets, and it conflicts with the product expectation of a betting page focused on currently available opportunities.

Steps:

1. Open the app with a valid `user-id`.
2. Observe the default `Upcoming Football Matches` list before applying filters.
3. Check the kickoff dates and ordering of the first visible events.
4. Apply today's date or a future date filter and compare the visible results.

Expected Result:

- Default view shows upcoming/pre-match football events only.
- Past/completed events are not shown in the primary betting list by default.
- If historical events are intentionally supported, they are separated into a clearly labeled archive or past-results view.
- Events are ordered in a way that surfaces the most relevant upcoming betting opportunities first.

## SBP-004: Stake Validation Boundaries in UI and API

Priority: High

Risk Rationale: Stake validation is money-handling validation. Boundary defects can cause rejected valid bets, accepted invalid bets, rounding discrepancies, or inconsistent client/server behavior.

Steps:

1. Select a valid match outcome.
2. Try stake values: blank, non-numeric text, `0.99`, `1.00`, `100.00`, `100.01`, and `10.999`.
3. Repeat representative invalid values directly through `/api/place-bet`.

Expected Result:

- UI blocks invalid stake values with clear messages.
- API rejects invalid stake values with appropriate `422` validation errors.
- Valid boundary values are accepted according to the clarified minimum and maximum rules.
- More than two decimal places is rejected by both UI and API.

## SBP-005: Single Selection Replacement and Removal

Priority: Medium

Risk Rationale: The feature supports single bets only. Multiple active selections would create accidental accumulator behavior, which is explicitly out of scope.

Steps:

1. Select HOME odds for one match.
2. Select DRAW or AWAY odds for a different match.
3. Inspect the bet slip.
4. Use per-selection remove.
5. Select another outcome and use `Remove All`.

Expected Result:

- New odds selection replaces the previous selection.
- Bet slip count remains `1`.
- Per-selection remove clears only the active selection.
- `Remove All` clears selection and stake.
- No multi-bet or accumulator state is possible.

## SBP-006: Date and Odds Filters Respect Inclusive Boundaries

Priority: Medium

Risk Rationale: Filters control event discoverability. Incorrect filter boundaries can hide valid markets or show unavailable markets, leading to user confusion and missed betting opportunities.

Steps:

1. Apply a single-day date filter.
2. Apply a date range filter.
3. Apply an odds range where min/max exactly match visible odds.
4. Enter an invalid odds range where min is greater than max.
5. Reset filters.

Expected Result:

- Date filters are inclusive.
- Odds filters are inclusive.
- Invalid ranges are rejected with clear feedback.
- Reset restores the default upcoming/pre-match event view.
