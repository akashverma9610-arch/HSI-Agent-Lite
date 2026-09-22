# Rotation comparison contract

Rotation is a governed comparison, not a score sort or transaction. Legacy
`CapitalRotationEngine` is analytical; Lite has no rotation runtime. A
candidate score of 8.9 versus incumbent 8.1, for example, is not enough.

| Comparable side | Required context |
| --- | --- |
| Incumbent | Current thesis and strategy fit; current, as-of evidence; remaining upside and downside; current-price **forward** R:R, not stale original-entry R:R; invalidation proximity; liquidity and portfolio role. |
| Candidate | Selected strategy fit and current evidence quality; catalyst, valuation, timing, entry/stop/invalidation, fresh-entry R:R, liquidity and portfolio fit. |
| Transition | Shared horizon, fees, taxes, slippage, opportunity cost, confirmation/cooldown, settlement/funding and cash availability. |

Compare like-with-like. Missing forward economics, inconsistent horizons,
stale/conflicted evidence, unmodeled friction/tax or unknown cash cannot be
silently filled. Candidate eligibility also needs the applicable six gates;
Gate FAIL or insufficient evidence blocks a purported edge. A replacement
must clear the governed hurdle after friction and portfolio constraints,
including heat/concentration. Ranking tie-breaks are not an action score.

Knowledge outputs are `KEEP_INCUMBENT`, `ROTATION_WORTH_REVIEW`,
`CASH_PREFERRED`, and `INSUFFICIENT_COMPARABLE_EVIDENCE`. Cash is a
legitimate alternative when no qualifying replacement exists; an unknown
cash balance is not zero and cannot be treated as available funding. Legacy
`ROTATE_CANDIDATE_PREFERRED` is only an analytical state and is not a
Lite trade instruction. Gate 1 V2 horizon/parcel-source blockers and the
Fast-Rotation proposal remain unresolved.
