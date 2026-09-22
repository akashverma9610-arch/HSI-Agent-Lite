# Governance knowledge extraction — Task #004

Source baseline: read-only `Hybrid-Stock-Intelligence` commit `f88b44d514fc9a2654040aa04e5350fc9e8660fe`. The nine JSON records in `hsi_knowledge/governance/` are extracted governance meaning, not runtime rules, diagnostics, strategies, thresholds, or live data. Each cited legacy file/heading was checked at that commit; `legacy_sources` in each record is the exact machine-readable provenance. The Task #002 manifest guided navigation but is not substituted for source review.

## Lifecycle and schema boundary

Task #003's `knowledge.schema.json` admits `governance_policy` but explicitly bars it from `APPROVED_FOR_LITE` and `ACTIVE` until a reviewed type-specific payload contract exists. Task #004 does not weaken that schema or relabel a governance record as a diagnostic/gate/strategy. Every record is therefore `REVIEW_REQUIRED`, `extraction_status=VERIFIED`, `review_status=IN_REVIEW`, with no effective date or runtime activation. This is narrower than legacy authority: the three authoritative legacy domains retain `AUTHORITATIVE_ACCEPTED` provenance but are not claimed to be active Lite policy. A future governance payload schema, explicit human review of each version, and lifecycle decision are required before promotion. The `details` objects are narrowly scoped declarative statements and have no calculation or broker authority.

## Extracted domains

### Evidence discipline (`AUTHORITATIVE_ACCEPTED`)

- Legacy: `docs/architecture/brain_contract.md#Brain Contract`; `docs/CLAIM_MODEL.md#Claim model`.
- Meaning: FACT → DATA → INTERPRETATION → INFERENCE. Source facts and normalized data are not model interpretation; inference remains qualified. Missing is UNKNOWN/UNAVAILABLE, never zero, neutral, PASS, or manufactured confidence.
- Lite may rely on this as an extraction constraint for future evidence and diagnostic contracts. It may not infer that any specific datum is certified or that a diagnostic has passed.
- Limitation: no runtime evidence validator exists in this task. Future consumer: evidence normalization and diagnostic eligibility.

### Source hierarchy (`AUTHORITATIVE_ACCEPTED`)

- Legacy: `docs/SOURCE_RELIABILITY.md#Source reliability`; `docs/CLAIM_MODEL.md#Claim model`; `docs/architecture/brain_contract.md#Brain Contract`.
- Meaning: distinguish exchange/regulatory/company statutory disclosure, audited/reported financial facts, official provider observations, reputable secondary reporting, and social/crowd evidence. Primary material outranks contradictory lower-tier claims. Same-event article repetition is not independent corroboration.
- Lite may rely on tier and claim-provenance discipline. It may not treat a producer's label as verified primary authority, a newer secondary article as an overwrite of a primary fact, or sentiment as business truth.
- Limitation: source identity/authenticity is not certified by this JSON. Future consumer: source resolver and claim deduplicator.

### Data reliability (`LATEST_ACCEPTED_WITH_LIMITATIONS`)

- Legacy: `docs/DATA_FRESHNESS.md#Market-data quality, freshness, and provenance`; `docs/architecture/PILOT_SOURCE_CURRENT_EOD_AND_HANDOFF_V1.md#Current EOD versus frozen history`; `app/data_operations/source_dependency_ledger.py#RetainedSourceReference`.
- Meaning: preserve source, publication/effective, receipt and ingestion times distinctly; evaluate freshness and quality per source family; missing or degraded input stays visible; fallback needs authority and must never be fabricated.
- Lite may rely on these metadata requirements. It may not infer universal freshness durations, source-family readiness, historical known-at from an EOD receipt, or P1 eligibility from operations success.
- Limitations: current EOD handoff is partial; exchange publication may be unknown. Future consumer: source-family quality/freshness evaluator.

### Historical PIT (`LATEST_ACCEPTED_WITH_LIMITATIONS`)

- Legacy: `app/historical/guard.py#BacktestLookaheadGuard.evaluate` and `#BacktestLookaheadGuard.membership`; `docs/HISTORICAL_DATASET.md#Historical Dataset`; `docs/reports/P1_PROSPECTIVE_HISTORY_RUNTIME_CLOSURE_2026-09-22.md#Source audit: implemented components versus missing proof`.
- Meaning: event, publication, receipt/known-at and effective time must be valid at replay cutoff; dated universe membership and price adjustment/corporate-action basis matter. No lookahead or present-day facts masquerading as historical availability.
- Lite may rely on fail-closed PIT eligibility requirements. It may not claim strict 61-diagnostic historical readiness or complete P1 per-input known-at proof.
- Limitations: source dependency closure and price-basis assurance remain gaps. Future consumer: historical replay/PIT guard.

### Model governance (`AUTHORITATIVE_ACCEPTED`)

- Legacy: `docs/architecture/model_governance.md#Model Governance and Drift`; `docs/STRATEGY_GOVERNANCE.md#Lifecycle and approval`.
- Meaning: proposal → research/OOS → eligibility → human review → immutable approved version → separate prospective activation, with governed rollback. Drift is an observation/recommendation, not deployment.
- Lite may rely on this promotion sequence. It may not infer approval of any candidate, auto-promote a model, or permit self-modifying live policy.
- Limitation: no candidate validation is performed here. Future consumer: version registry and activation reviewer.

### Prospective validation (`LATEST_ACCEPTED_WITH_LIMITATIONS`)

- Legacy: `docs/OUT_OF_SAMPLE_VALIDATION.md#Out-of-Sample Validation`; `docs/WALK_FORWARD_VALIDATION.md#Walk-Forward Validation`; `docs/architecture/COMPOUNDER_PROSPECTIVE_SHADOW_VALIDATION_V1.md#Decision and boundary`.
- Meaning: historical research, backtest, walk-forward, OOS, research shadow, prospective observation and production activation are distinct. TEST partitions and capital are isolated; OOS success is evidence, not approval.
- Lite may rely on separation and lineage. It may not equate historical success, a shadow record, or prospective observation with product qualification or activation.
- Limitation: research-shadow and source coverage do not close product readiness. Future consumer: validation ledger and activation gate.

### Signal Watch (`LATEST_ACCEPTED_WITH_LIMITATIONS`)

- Legacy: `docs/architecture/POST_V1_HSI_SIGNAL_P1_ACTIVATION_PROPOSAL.md#Status`; `docs/architecture/SIGNAL_LIFECYCLE_P1_RUNTIME_BINDING_V1.md#Strict source trust boundary and live limitation`; `docs/reports/P1_PROSPECTIVE_HISTORY_RUNTIME_CLOSURE_2026-09-22.md#Source audit`.
- Meaning: P1 is `WATCH_ONLY / NON_EXECUTABLE`; an internal on-demand projection and isolated lifecycle mechanics are not consumer activation. Signal existence does not grant order authority.
- Lite may rely on these safety labels. It may not claim production wiring, consumer activation, or complete source known-at lineage.
- Limitation: owning-source adapter and dependency closure remain unavailable. Future consumer: governed Watch reader.

### Strategy registry (`LATEST_ACCEPTED_WITH_LIMITATIONS`)

- Legacy: `app/intelligence/hsi_signal_strategy_registry.py#HSI_SIGNAL_STRATEGY_REGISTRY_ID`; `docs/architecture/POST_V1_STRATEGY_AND_SIGNAL_WINDOW_CATALOGUE.md#Capability-status matrix`; `docs/STRATEGY_VERSIONING_AND_ACTIVATION.md#Strategy Versioning and Activation`.
- Meaning: registry identity, version, provenance and availability are distinct from policy approval and activation. An unavailable strategy stays `STRATEGY_UNAVAILABLE`.
- Lite may rely on fail-closed resolution semantics. It may not turn catalogue membership, implemented evidence, a Watch, a setup, score or gate into an active product strategy.
- Limitation: Post-V1 catalogue is product scope, not approved strategy policy. Future consumer: read-only policy resolver.

### Macro/news governance (`LATEST_ACCEPTED_WITH_LIMITATIONS`)

- Legacy: `docs/architecture/economic_news_intelligence.md#Economic and News Intelligence`; `docs/architecture/CATALYST_EVENT_INTELLIGENCE_OPERATIONAL_CLOSURE_V1.md#Architecture and approved boundaries` and `#Inventory and readiness`.
- Meaning: macro/news is contextual evidence; preserve event identity and source provenance; prove sector/company transmission before asserting impact. Repeated articles or the same event ID are not separate confirmations.
- Lite may rely on context and deduplication requirements. It may not derive a Macro/News score, direct BUY/SELL, company benefit, event direction, or Event/Catalyst strategy parameters.
- Limitations: source coverage, freshness, cross-producer reconciliation and company transmission are partial. Future consumer: macro/news context assembler.

All prospective consumers are proposals for where the contracts would be checked later; none are implemented by Task #004. No broker-order authority is conferred.
