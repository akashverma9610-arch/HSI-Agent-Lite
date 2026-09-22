# V1 61-diagnostic knowledge extraction — Task #005

The read-only legacy source is `Hybrid-Stock-Intelligence` at `f88b44d514fc9a2654040aa04e5350fc9e8660fe`. The primary identity and names are `app/registry/canonical.py#DIAGNOSTIC_RULES`; the committed operational audit is `docs/architecture/DIAGNOSTIC_61_OPERATIONAL_COVERAGE_V1.json#records`. Task #002's duplication audit maps legacy call paths. Each catalog record retains its exact source pointers and V1 label. This extraction defines knowledge and future ownership, not a running evaluator.

## Count, domains and lifecycle

There are exactly **61** V1 JSON artifacts, one for each canonical ID D01–D61, and one index row per artifact.

| Reading group | IDs | Count |
| --- | --- | ---: |
| Market / Sector / Structure | D01–D14 | 14 |
| Business / Fundamental / Governance | D15–D30 | 16 |
| Synthesis / Scenario / Value | D31–D39 | 9 |
| Trade Geometry | D40–D46 | 7 |
| Crowd / Liquidity / Contrarian | D47–D61 | 15 |

Task #002 legacy audit categories are preserved exactly: 27 `PURE_CONSUMER`, 10 `JUSTIFIED_UNIQUE_CHECK`, 22 `DUPLICATE_COMPUTATION`, one `CONFLICTING_AUTHORITY`, one `UNKNOWN_NEEDS_EXTRACTION`. The Lite *future evaluation types* are different by design: 41 `PURE_CONSUMER`, eight `COMPOSITE_RECONCILIATION`, ten `JUSTIFIED_UNIQUE_CHECK`, and two `UNRESOLVED`. The 22 duplicates are provenance findings, not approved Lite recomputation behavior.

Fifty-nine V1 artifacts have `LATEST_ACCEPTED_WITH_LIMITATIONS` legacy authority and `REVIEW_REQUIRED` Lite lifecycle. D35 and D57 have `CONFLICT_REVIEW_REQUIRED` and `QUARANTINED`. All have `review_status=IN_REVIEW`, no effective date, no Lite calculation owner, and no ACTIVE status. Their `criticality=NON_CRITICAL` means only that this extraction assigns no *direct gate criticality*; the legacy registry has no rule-level criticality field. It is not a claim that an eventual gate may ignore a required input.

## Evidence ownership and normalization

`EVIDENCE_DEPENDENCY_CATALOG.json` lists 50 logical normalized evidence families, their conceptual owners, legacy sources, requirements, consumers and unresolved semantics. `CALCULATION_OWNER_MAP.json` identifies 42 deterministic metric families with one future conceptual owner each. Neither file stores market observations, approved parameter values, executable formulas or runtime bindings. The seven regression families—`base_pattern`, `liquidity_pools`, `ichimoku`, `crowd_sentiment`, `rvol`, `sector_health`, and `quarterly_growth`—each have exactly one owner entry.

The target flow is **one calculation owner → one versioned normalized evidence record → many diagnostic consumers**. Future evidence records must carry instrument, timeframe, source, parameters and as-of identity under Task #003's contract. A composite diagnostic can reconcile already-normalized records but cannot recalculate their component metrics. Every catalog record has explicit PASS, CAUTION, FAIL and UNKNOWN descriptions. Legacy V1 has `NEUTRAL`, `INSUFFICIENT_DATA` and `UNVERIFIED`, not a native CAUTION state; CAUTION therefore remains a future reviewed mapping, not a fabricated result. Missing, stale, conflicting, noncomparable or uncertified evidence is UNKNOWN, never PASS or neutral.

The evidence catalog also states normalized upstream dependencies for the known nested families (for example, sector rotation reads sector health, volume climax reads RVOL, and target geometry reads the base pattern). This is an acyclic conceptual graph, not an implementation of those calculations.

## All 22 legacy duplicate-path transformations

The audit's repeated work does **not** prove incorrect legacy outputs. The table states the future consumer boundary; no runtime removal or calculation code exists yet.

| ID | Legacy repeated helper / metric | Future normalized evidence IDs | Diagnostic-specific interpretation retained | Lite responsibility |
| --- | --- | --- | --- | --- |
| D03 | SV:sector_rotation→sector_health — Same sector health/excess | sector_health, sector_rotation | Sector rotation phase; Derive phase from Rule 2 owner evidence; do not rerun return. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D05 | EV:weinstein; overlapping TE:sma — Weekly close, moving average and slope | moving_average_structure, trend_weekly | Weinstein stage; One technical MA/stage owner; diagnostic consumes result. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D07 | LI:smart_money→accumulation_distribution — Price/volume accumulation proxy | accumulation_distribution | Smart-money proxy; Reuse normalized accumulation proxy; never claim institution identity. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D09 | LI:wyckoff→events→pools — Price range plus liquidity event | liquidity_pools, liquidity_events, wyckoff_phase | Wyckoff phase; Consume pool/event evidence, then phase interpretation. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D13 | EV:chikou→SV:ichimoku — Chikou field of Ichimoku output | ichimoku | Chikou confirmation; Consume same timeframe Ichimoku record. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D14 | SV:multi_timeframe_alignment→ichimoku; EV:mtf — Distinct frame Ichimoku states | ichimoku | Multi-timeframe alignment; Reconcile keyed per-frame indicator records; fail closed on missing frames. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D25 | FU:latest_quarter; FC input certification — Revenue/EBITDA/PAT/EPS YoY/QoQ | quarterly_growth, financial_comparability | Latest quarter; Share certified quarterly growth series across 24/25. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D38 | VT:pullback→base_pattern — Base support and close | base_pattern, pullback | Pullback quality; Consume one base-pattern record. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D40 | VT:aggressive_entry→base_pattern — Base resistance/support | base_pattern, entry_geometry | Aggressive entry; Consume strategy-scoped base; keep candidate non-executable. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D41 | VT:confirmation_entry→base_pattern — Base resistance and completed close | base_pattern, entry_geometry | Confirmation entry; Reuse base and close evidence under selected strategy policy. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D42 | VT:retest_entry→pullback→base_pattern — Pullback/support | base_pattern, pullback, entry_geometry | Retest entry; Reuse base and pullback evidence. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D43 | VT:structural_stop→pullback→base_pattern — Pullback/support | base_pattern, pullback, stop_geometry | Structural stop; One strategy-specific stop geometry owner. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D44 | VT:targets→base_pattern — Base height/resistance | base_pattern, target_geometry | T1/T2/Extended; One strategy-specific target geometry owner. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D46 | VT:invalidation→structural_stop→pullback→base_pattern — Structural support/stop | base_pattern, stop_geometry | Thesis invalidation; Consume selected stop/support; keep fundamental invalidation separate. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D50 | LI:accumulation_distribution→events,wyckoff — Price, events, Wyckoff proxy | accumulation_distribution, liquidity_events, wyckoff_phase | Accumulation/distribution; Reuse normalized event/phase outputs; no institutional-flow claim. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D51 | LI:stop_clusters→pools — Pool map | liquidity_pools | Stop clusters; Derive cluster interpretation from one pool record. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D52 | LI:events→pools — Pool map plus current bar | liquidity_pools, liquidity_events | Liquidity events; Reuse pool map and bar; absorption stays unavailable without book. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D53 | LI:bull_trap→pools — Pool map plus price/volume | liquidity_pools, trap_evidence | Bull trap; Reuse pool map and trap evidence. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D54 | LI:bear_trap→pools — Pool map plus price/volume | liquidity_pools, trap_evidence | Bear trap; Reuse pool map and trap evidence. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D55 | CR:trap_probability→sentiment,confidence,divergence — Sentiment, confidence, divergence | crowd_sentiment, crowd_data_confidence, crowd_divergence, crowd_trap | Crowd trap probability; Consume Rules 47/49/56 evidence; retain uncalibrated label. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D56 | CR:divergence→sentiment — Sentiment and aligned price | crowd_sentiment, crowd_divergence | Price/crowd divergence; Consume one sentiment record plus price. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |
| D58 | LI:volume_climax; overlap SV:volume_rvol — RVOL, range, close location | rvol, volume_climax | Volume climax; One normalized RVOL definition, then climax-specific check. | Upstream metric is owned by its evidence family; no diagnostic helper re-run. |

## V1 authority and pending V2

D16, D17, D19, D25, D26 and D29 retain the active/latest usable **V1** canonical names and meanings. `docs/architecture/FUNDAMENTAL_DIAGNOSTIC_REGISTRY_V2_GOVERNANCE_APPROVAL.md#Authority, identity and scope` approved successor semantics but explicitly did **not** activate V2. Each affected artifact cites that receipt and carries an inactive-successor limitation. No V2 artifact or version is activated here.

Fundamental evidence must preserve scope, period basis, units/scale and comparability. Missing denominators, CAPEX, valid periods, forward inputs or source facts are not zero. The older financial adapter may be lossy; `financial_comparability` is a shared dependency, not a substitute source or second formula owner.

## Quarantine

- **D35 VWAP & Value Area Acceptance:** named VWAP/value-area source semantics are not proven by the generic fallback. `CONFLICT_REVIEW_REQUIRED / QUARANTINED / UNRESOLVED`; no named stream or PASS/FAIL invented.
- **D57 Post-News Price Reaction:** canonical event identity, materiality/polarity, known-at and completed-session join remain unresolved. `CONFLICT_REVIEW_REQUIRED / QUARANTINED / UNRESOLVED`; legacy audit class `UNKNOWN_NEEDS_EXTRACTION`. News rows alone do not certify this diagnostic.

## Operational limits and non-claims

The legacy closure measured 29 current-descriptive ready, 18 partial and 14 not ready at its dated audit; no full 61-rule production materialization, full prospective PIT coverage, or strict historical PIT readiness follows. A wrapper, implementation path, unit test or source snapshot is not product eligibility. The index's score-component references are descriptive lineage only; this task computes no Decision Score or weight, invokes no gate, approves no strategy and grants no broker/order authority. No indicator, fundamental, valuation, market, RAG, API or agent runtime is implemented.
