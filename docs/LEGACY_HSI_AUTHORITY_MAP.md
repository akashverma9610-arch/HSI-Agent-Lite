# Legacy HSI authority map — Task #002

All paths and conclusions are pinned to committed legacy HEAD `f88b44d514fc9a2654040aa04e5350fc9e8660fe`; exact source paths/symbols and domain details are in [the inventory](LEGACY_HSI_KNOWLEDGE_INVENTORY.md) and `hsi_knowledge/LEGACY_SOURCE_MANIFEST.yaml`. The local HEAD is two clean commits newer than the expected `810590be` ancestor. Authority is assigned by closure/approval receipts, then contracts, implementation, tests and older drafts. An approved definition can be non-active; an implemented component can be unready for a consumer.

| Domain | Classification | Authority decision and supersession boundary |
| --- | --- | --- |
| `diagnostics_61` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | V1 `app/registry/canonical.py#DIAGNOSTIC_RULES` defines 61 IDs; operational closure is partial. V2 changes six definitions but remains inactive. |
| `decision_score_10` | `AUTHORITATIVE_ACCEPTED` | `app/scoring/engine.py#COMPONENTS,build_scorecard` is the ten-component 0–10 score owner; missing mandatory inputs block completion. |
| `six_gates` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | `app/gates/production_policy.py#POLICY_ID` V1 active; V2.4 approval is semantic only with activation blockers. |
| `pre_breakout` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | Governed Pre-Breakout policy/setup exists; selected version and complete P1 source known-at still matter. Drafts are subordinate to approval/selection. |
| `tactical` | `PROPOSED_NOT_ACTIVE` | Product catalogue has no approved Tactical strategy policy; technical functions are reusable evidence only. |
| `positional` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | Pre-Breakout is one governed positional instance; general positional product strategy remains unavailable. |
| `long_term` | `PROPOSED_NOT_ACTIVE` | Rule 33 and research shadows are not a Long-Term family strategy. Family policy pack is proposed and product families remain unavailable. |
| `event_catalyst` | `PROPOSED_NOT_ACTIVE` | Event evidence path is operational with source gaps; Batch 1 strategy parameters and calibration remain unresolved. |
| `market_red_resilience` | `PROPOSED_NOT_ACTIVE` | MR evidence boundaries approved, but historical inputs and operational parameters are insufficient. |
| `market_extremes` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | Core downside/upside context exists; Post-V1 assurance projection is a non-active future consumer, not a new regime owner. |
| `macro_news` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | Evidence-first context is accepted; source/coverage and transmission are partial; no Macro/News score or direct action. |
| `liquidity_exitability` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | Core liquidity proxies are implemented; no universal exitability policy/clearance may be inferred. |
| `entry` | `CONFLICT_REVIEW_REQUIRED` | Generic Rules 40–42 and governed Pre-Breakout entry have different policy scope; proposed grid/trigger changes need explicit selection. |
| `stop_invalidation` | `CONFLICT_REVIEW_REQUIRED` | Rule 43/46 price structure and Pre-Breakout tick/support differ; long-term fundamental/catalyst invalidation remains undefined. |
| `targets` | `CONFLICT_REVIEW_REQUIRED` | Generic Rule 44 target hierarchy, Pre-Breakout measured target and Gate 4 tranche context must remain versioned by owner. |
| `trim_profit` | `PROPOSED_NOT_ACTIVE` | Portfolio sell-side approval explicitly says `TRIM_NOT_AUTHORIZED_V1`; Profit-Harvesting has no approved product policy. |
| `portfolio_health` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | Immutable portfolio/cash/holding analysis is accepted; sell-side decision policy approved but not selected or active. |
| `portfolio_rotation` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | Core analytical comparison accepted; Gate-1 V2 horizon/parcel source blockers and Fast-Rotation product status remain separate. |
| `data_reliability` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | Quality/freshness/source lineage contracts accepted; current EOD handoff and complete source readiness are partial. |
| `source_hierarchy` | `AUTHORITATIVE_ACCEPTED` | Tiered primary-over-secondary reliability contract is accepted; source labels alone do not prove authenticity. |
| `evidence_discipline` | `AUTHORITATIVE_ACCEPTED` | Brain contract fixes FACT → DATA → INTERPRETATION → INFERENCE and fail-closed missing data. |
| `historical_pit` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | PIT and lifecycle guards are accepted; strict historical diagnostic coverage and P1 complete dependency known-at proof are not. |
| `model_governance` | `AUTHORITATIVE_ACCEPTED` | Immutable experiment/OOS/human approval/activation/rollback chain; drift is observation, never deployment. |
| `prospective_validation` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | OOS and walk-forward contracts accepted; prospective shadow evidence does not activate a product or close source history gaps. |
| `signal_watch` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | P1 projection is Watch-only, internal/on-demand; lifecycle mechanics isolated and not production-wired. |
| `strategy_registry` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | Core/P1 provenance registry exists; Post-V1 catalogue is future scope, not an active strategy registry of approved product policies. |
| `market_regime` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | Deterministic V1 classification exists; mock threshold set is not production calibrated. |
| `sector_context` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | Exact mapping/sector OHLC subset exists; dated 61-rule audit shows incomplete coverage and no fund-flow authority. |
| `relative_strength` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | Stock/benchmark relative evidence exists; authoritative peer cohorts and historical resilience eligibility are unproved. |
| `risk_reward` | `LATEST_ACCEPTED_WITH_LIMITATIONS` | Rule 45 geometry and rotation checks exist; a score or generic R:R alone cannot override gates or strategy-specific entry. |

## Decisions that prevent false promotion

- `docs/architecture/FUNDAMENTAL_DIAGNOSTIC_REGISTRY_V2_GOVERNANCE_APPROVAL.md#Authority, identity and scope` records **V1 active, V2 inactive**. Its six changed IDs are 16, 17, 19, 25, 26 and 29; the other 55 inherit V1. The newer shadow bridge and version-compatibility repairs do not change this.
- `docs/architecture/EXECUTION_GATE_POLICY_V2_COMPOSITE_GOVERNANCE_APPROVAL_2.md#Single successor` makes V2.4 the single future whole-policy candidate. Older V2.2/V2.3 component approvals are historical; V2.4 has no runtime effective date and cannot displace active V1.
- `docs/architecture/POST_V1_STRATEGY_AND_SIGNAL_WINDOW_CATALOGUE.md#Authority and status language` is approved as product *scope* but explicitly not as approved strategy policy. Pre-Breakout is `POLICY_AVAILABLE`; the other named product families are `STRATEGY_UNAVAILABLE`.
- `docs/architecture/POST_V1_BATCH_1_HISTORICAL_CALIBRATION_RESEARCH.md#Data-readiness matrix` reports insufficient Event/Catalyst and Market-Red calibration. The architectural boundary approval is not a parameter selection.
- `docs/architecture/PORTFOLIO_SELL_SIDE_DECISION_POLICY_V1_APPROVAL.md#Deferred policy gaps` approves a narrow policy artifact but marks it not selected/active and forbids trim. `app/intelligence/sell_risk_review_policy.py` is a separate Watch-only research review, not a SELL producer.
- `docs/reports/P1_PROSPECTIVE_HISTORY_RUNTIME_CLOSURE_2026-09-22.md#Source audit` records an unresolved owning-source dependency/known-at adapter. Stored assessments and test fixtures do not prove a real prospective P1 admission.

No source in this map is promoted solely by a recent filename, passing unit test, proposal, implementation, or historical data count. Where an exact active strategy-specific rule is not established, Lite must keep the domain unresolved rather than synthesize a threshold.
