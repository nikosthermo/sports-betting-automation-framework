# Test Plan: Single Bet Placement

## SBP-001: Place a Valid Single Bet

Priority: Critical

Risk Rationale: This is the primary revenue-generating journey. Incorrect selection, stake, payout, or receipt data can directly affect user trust and financial correctness.

Steps:

1. Open the app with a valid `user-id`.
2. Confirm balance is shown as EUR.
3. Select the HOME odds for the first upcoming match.
4. Enter stake `10.00`.
5. Verify potential payout equals `stake * selected odds`.
6. Click `Place Bet`.
7. Verify success receipt.

Expected Result:

- Button enters `Placing...` state.
- Balance is reduced by `€10.00`.
- Receipt shows bet id, correct home-vs-away match order, HOME selection, stake, odds at placement, payout, and timestamp.
- Closing the receipt returns to the main flow with no active selection.

## SBP-002: API Rejects Invalid Stake Precision

Priority: Critical

Risk Rationale: Money values must be deterministic. Accepting more than two decimals can create rounding and reconciliation defects.

Steps:

1. Fetch an existing match from `/api/matches`.
2. POST `/api/place-bet` with valid `matchId`, selection `HOME`, and stake `10.999`.

Expected Result:

- API returns `422`.
- Response identifies invalid stake precision.
- No balance is deducted.

## SBP-003: Stake Cannot Exceed Available Balance

Priority: High

Risk Rationale: Allowing users to stake beyond balance creates financial exposure and breaks wallet integrity.

Steps:

1. Reset balance.
2. Select any odds.
3. Enter a stake greater than the displayed balance.
4. Attempt to place the bet.

Expected Result:

- UI blocks placement.
- User sees `Insufficient balance`.
- API also rejects an equivalent direct request.

## SBP-004: Single Bet Selection Replacement

Priority: High

Risk Rationale: The feature supports only one active bet. Multiple active selections would create accidental multi-bets, which are explicitly out of scope.

Steps:

1. Select HOME odds for one match.
2. Select AWAY odds for another match.
3. Inspect the bet slip.

Expected Result:

- The second selection replaces the first.
- Bet slip count remains `1`.
- Only the latest selected match and outcome are shown.

## SBP-005: Stake Boundary Validation

Priority: Medium

Risk Rationale: Boundary defects are common in payment-like inputs and can produce inconsistent UI/API behavior.

Steps:

1. Select any odds.
2. Try stake `0.99`.
3. Try stake `1.00`.
4. Try stake `100.00`.
5. Try stake `100.01`.

Expected Result:

- `0.99` is rejected with minimum stake messaging.
- `1.00` is accepted if the clarified minimum is `€1.00`.
- `100.00` is accepted.
- `100.01` is rejected with maximum stake messaging.

## SBP-006: Odds Filter Invalid and Inclusive Ranges

Priority: Medium

Risk Rationale: Filtering affects discoverability and selection accuracy. Invalid range handling must be clear to avoid hiding valid betting options.

Steps:

1. Open the odds filter.
2. Apply a valid min/max range matching known odds.
3. Confirm matches with odds inside the range are shown.
4. Enter a min value greater than max.
5. Apply the invalid range.

Expected Result:

- Valid ranges are inclusive.
- Invalid ranges are rejected with clear feedback.
- Existing results are not silently corrupted.
