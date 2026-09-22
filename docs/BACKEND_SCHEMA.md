# Backend Schema — HSI Agent Lite

## 1. Purpose

This document defines the planned logical backend schema for HSI Agent Lite. It is a design contract, not an Alembic migration. Final SQL types/indexes may evolve during implementation, but ownership, lineage, user isolation and calculate-once semantics should be preserved.

PostgreSQL is the primary relational store. Version-controlled knowledge under `hsi_knowledge/` remains outside mutable runtime tables except for optional indexed registry snapshots.

## 2. Design principles

1. Canonical security identity is referenced everywhere by `security_id`.
2. Raw facts, normalized evidence, diagnostics and conclusions are separate layers.
3. Deterministic evidence is stored once per input/version fingerprint and reused.
4. Every analysis result is linked to an `analysis_run_id`.
5. User portfolio rows are isolated by authenticated `user_id`.
6. Source/provenance timestamps remain explicit.
7. UNKNOWN is represented as state/null, never fabricated numeric zero.
8. Strategy/gate/score policy versions are persisted with outputs.
9. No table grants broker-order authority.

## 3. Identity and access

### users
- id UUID PK
- auth_subject TEXT UNIQUE NOT NULL
- display_name TEXT NULL
- role TEXT NOT NULL
- status TEXT NOT NULL
- created_at TIMESTAMPTZ
- updated_at TIMESTAMPTZ

### user_preferences
- user_id UUID PK/FK users
- default_universe JSONB
- default_market_cap_min NUMERIC NULL
- default_market_cap_max NUMERIC NULL
- research_preferences JSONB
- created_at / updated_at

## 4. Security master

### securities
- id UUID PK
- exchange TEXT
- symbol TEXT
- isin TEXT NULL
- company_name TEXT
- instrument_type TEXT
- listing_status TEXT
- sector_id UUID NULL
- active_from DATE NULL
- active_to DATE NULL
- identity_status TEXT
- created_at / updated_at

Unique candidates:
- exchange + symbol + active_from
- isin where non-null

### security_aliases
- id UUID PK
- security_id UUID FK
- alias_type TEXT
- alias_value TEXT
- effective_from TIMESTAMPTZ NULL
- effective_to TIMESTAMPTZ NULL
- source_id UUID NULL

### sectors
- id UUID PK
- code TEXT UNIQUE
- name TEXT
- benchmark_security_id UUID NULL
- parent_sector_id UUID NULL

## 5. Source and provenance

### sources
- id UUID PK
- source_code TEXT UNIQUE
- source_name TEXT
- source_tier TEXT
- provider TEXT NULL
- authority_class TEXT
- active BOOLEAN
- metadata JSONB

### source_observations
- id UUID PK
- source_id UUID FK
- security_id UUID NULL
- observation_type TEXT
- publication_time TIMESTAMPTZ NULL
- receipt_time TIMESTAMPTZ NULL
- effective_time TIMESTAMPTZ NULL
- ingestion_time TIMESTAMPTZ NOT NULL
- source_locator TEXT NULL
- payload_hash TEXT
- raw_payload_ref TEXT NULL
- quality_state TEXT
- freshness_state TEXT
- conflict_state TEXT
- metadata JSONB

Index strongly on security_id, observation_type, effective_time/as-of fields.

## 6. Market and financial raw/normalized data

### market_bars
- security_id UUID
- timeframe TEXT
- bar_time TIMESTAMPTZ
- open/high/low/close NUMERIC
- volume NUMERIC NULL
- traded_value NUMERIC NULL
- delivery_volume NUMERIC NULL
- price_basis TEXT
- source_observation_id UUID
- quality_state TEXT
- PRIMARY KEY (security_id, timeframe, bar_time, source_observation_id)

### corporate_actions
- id UUID PK
- security_id UUID FK
- action_type TEXT
- announcement_time TIMESTAMPTZ NULL
- ex_date DATE NULL
- effective_time TIMESTAMPTZ NULL
- factor NUMERIC NULL
- source_observation_id UUID
- status TEXT
- metadata JSONB

### financial_periods
- id UUID PK
- security_id UUID FK
- period_type TEXT
- period_start DATE NULL
- period_end DATE
- reported_at TIMESTAMPTZ
- statement_scope TEXT
- currency TEXT
- unit_scale TEXT
- source_observation_id UUID
- comparability_state TEXT

### financial_metrics
- financial_period_id UUID FK
- metric_code TEXT
- value NUMERIC NULL
- value_state TEXT
- metadata JSONB
- PRIMARY KEY (financial_period_id, metric_code)

## 7. Tool execution and evidence registry

### tool_definitions
- tool_id TEXT
- tool_version TEXT
- tool_family TEXT
- deterministic BOOLEAN
- calculation_owner BOOLEAN
- cost_class TEXT
- active BOOLEAN
- metadata JSONB
- PRIMARY KEY (tool_id, tool_version)

### tool_runs
- id UUID PK
- analysis_run_id UUID NULL
- tool_id TEXT
- tool_version TEXT
- security_id UUID NULL
- as_of TIMESTAMPTZ
- input_fingerprint TEXT
- status TEXT
- started_at TIMESTAMPTZ
- completed_at TIMESTAMPTZ NULL
- error_code TEXT NULL
- metadata JSONB

Recommended unique reuse key for deterministic runs:
- tool_id
- tool_version
- security_id
- as_of
- input_fingerprint

### evidence_records
- id UUID PK
- security_id UUID NULL
- evidence_family TEXT NOT NULL
- evidence_key TEXT NOT NULL
- as_of TIMESTAMPTZ NOT NULL
- value_json JSONB
- value_numeric NUMERIC NULL
- value_text TEXT NULL
- state TEXT NOT NULL
- quality_state TEXT
- freshness_state TEXT
- conflict_state TEXT
- source_lineage JSONB
- source_observation_ids JSONB
- owner_tool_id TEXT
- owner_tool_version TEXT
- computation_id TEXT NULL
- computation_version TEXT NULL
- input_fingerprint TEXT
- created_at TIMESTAMPTZ

Recommended uniqueness:
`security_id + evidence_key + as_of + owner_tool_id + owner_tool_version + input_fingerprint`

### evidence_dependencies
- evidence_id UUID FK evidence_records
- upstream_evidence_id UUID FK evidence_records
- relationship TEXT
- PRIMARY KEY (evidence_id, upstream_evidence_id)

## 8. Analysis runs

### analysis_runs
- id UUID PK
- user_id UUID FK
- run_type TEXT
- security_id UUID NULL
- universe_run_id UUID NULL
- requested_as_of TIMESTAMPTZ
- status TEXT
- knowledge_version TEXT
- diagnostic_registry_version TEXT
- score_policy_version TEXT NULL
- gate_policy_version TEXT NULL
- strategy_registry_version TEXT NULL
- created_at TIMESTAMPTZ
- completed_at TIMESTAMPTZ NULL
- request_metadata JSONB
- limitations JSONB

Run types may include ANALYSE, SCAN_CANDIDATE, WATCH_REFRESH, PORTFOLIO_REVIEW and REPLAY.

## 9. Diagnostics

### diagnostic_results
- id UUID PK
- analysis_run_id UUID FK
- security_id UUID
- diagnostic_id TEXT
- diagnostic_version TEXT
- result_state TEXT
- score_value NUMERIC NULL
- confidence_state TEXT NULL
- evidence_ids JSONB
- limitations JSONB
- explanation JSONB
- created_at TIMESTAMPTZ

Unique:
- analysis_run_id + diagnostic_id

D35/D57 and future quarantined diagnostics can remain UNKNOWN/UNAVAILABLE without fake scores.

## 10. Global score

### score_results
- id UUID PK
- analysis_run_id UUID FK UNIQUE
- policy_id TEXT
- policy_version TEXT
- scale_min NUMERIC
- scale_max NUMERIC
- final_score NUMERIC NULL
- completeness_state TEXT
- component_results JSONB
- mandatory_missing JSONB
- optional_missing JSONB
- created_at TIMESTAMPTZ

A null final_score is valid when mandatory dependencies are unavailable.

## 11. Execution gates

### gate_results
- id UUID PK
- analysis_run_id UUID FK
- gate_id TEXT
- gate_version TEXT
- outcome TEXT
- blocking BOOLEAN
- evidence_ids JSONB
- reason_codes JSONB
- limitations JSONB
- created_at TIMESTAMPTZ

Unique:
- analysis_run_id + gate_id

No score/LLM override column should exist as an authority mechanism.

## 12. Strategy taxonomy and evaluation

### strategy_archetype_registry
Optional database snapshot/index of version-controlled knowledge:
- archetype_id TEXT
- version TEXT
- primary_family TEXT
- lifecycle TEXT
- active_for_runtime BOOLEAN
- knowledge_hash TEXT
- metadata JSONB
- PRIMARY KEY (archetype_id, version)

### strategy_evaluations
- id UUID PK
- analysis_run_id UUID FK
- archetype_id TEXT
- archetype_version TEXT
- evaluation_state TEXT
- future_strategy_score NUMERIC NULL
- matched BOOLEAN NULL
- required_evidence_state TEXT
- evidence_ids JSONB
- diagnostic_ids JSONB
- gate_context JSONB
- why_now_state TEXT NULL
- timing_state TEXT NULL
- limitations JSONB
- created_at TIMESTAMPTZ

Unique:
- analysis_run_id + archetype_id + archetype_version

The initial runtime may leave future_strategy_score null until a governed policy exists.

### strategy_confluence_results
- id UUID PK
- analysis_run_id UUID FK UNIQUE
- state TEXT
- matched_archetypes JSONB
- overlap_summary JSONB
- independent_pairs JSONB
- unresolved_pairs JSONB
- evidence_lineage_fingerprint TEXT NULL
- created_at TIMESTAMPTZ

Confluence is not raw match count.

## 13. Discovery / whole-NSE scanning

### universe_runs
- id UUID PK
- user_id UUID FK
- universe_definition JSONB
- as_of TIMESTAMPTZ
- status TEXT
- created_at / completed_at

### universe_members
- universe_run_id UUID FK
- security_id UUID FK
- membership_state TEXT
- exclusion_reason TEXT NULL
- PRIMARY KEY (universe_run_id, security_id)

### discovery_gate_results
- id UUID PK
- universe_run_id UUID FK
- security_id UUID FK
- discovery_gate_id TEXT
- outcome TEXT
- reason_codes JSONB
- evidence_ids JSONB
- created_at TIMESTAMPTZ

Discovery gate IDs must be separate from GATE_1...GATE_6 execution IDs.

### detector_results
- id UUID PK
- universe_run_id UUID FK
- security_id UUID FK
- detector_id TEXT
- detector_version TEXT
- archetype_id TEXT
- triggered BOOLEAN
- evidence_ids JSONB
- trigger_reasons JSONB
- cost_class TEXT
- created_at TIMESTAMPTZ

### candidate_union
- universe_run_id UUID FK
- security_id UUID FK
- triggered_archetypes JSONB
- detector_result_ids JSONB
- evidence_identity_fingerprint TEXT
- preliminary_state TEXT
- PRIMARY KEY (universe_run_id, security_id)

## 14. Events / research

### events
- id UUID PK
- canonical_event_key TEXT UNIQUE
- security_id UUID NULL
- event_type TEXT
- event_time TIMESTAMPTZ NULL
- known_at TIMESTAMPTZ NULL
- source_observation_ids JSONB
- dedup_state TEXT
- metadata JSONB

### research_findings
- id UUID PK
- analysis_run_id UUID FK
- agent_type TEXT
- security_id UUID NULL
- finding_type TEXT
- statement TEXT
- support_state TEXT
- evidence_ids JSONB
- source_observation_ids JSONB
- model_provider TEXT
- model_name TEXT
- prompt_version TEXT
- created_at TIMESTAMPTZ

AI-generated interpretations must retain supporting evidence/source references.

## 15. Why-now, timing, risk/reward and delivery

### opportunity_context
- analysis_run_id UUID PK/FK
- why_now_state TEXT NULL
- why_now_evidence_ids JSONB
- timing_state TEXT NULL
- regime_compatibility_state TEXT NULL
- risk_reward_state TEXT NULL
- risk_reward_payload JSONB
- portfolio_fit_state TEXT NULL
- delivery_bucket TEXT NULL
- limitations JSONB

This table is analytical only. `delivery_bucket` must not imply broker execution authority.

## 16. Portfolios

### portfolios
- id UUID PK
- user_id UUID FK
- name TEXT
- status TEXT
- base_currency TEXT
- created_at / updated_at

### portfolio_positions
- id UUID PK
- portfolio_id UUID FK
- security_id UUID FK
- quantity NUMERIC
- average_cost NUMERIC NULL
- opened_at TIMESTAMPTZ NULL
- position_state TEXT
- updated_at TIMESTAMPTZ

Unique active-position policy should be decided during implementation.

### portfolio_cash
- portfolio_id UUID
- currency TEXT
- amount NUMERIC NULL
- as_of TIMESTAMPTZ
- state TEXT
- PRIMARY KEY (portfolio_id, currency, as_of)

Unknown cash is not zero.

### portfolio_snapshots
- id UUID PK
- portfolio_id UUID FK
- as_of TIMESTAMPTZ
- total_value NUMERIC NULL
- cash_value NUMERIC NULL
- positions_value NUMERIC NULL
- source_state TEXT
- metadata JSONB

### holding_health_results
- id UUID PK
- analysis_run_id UUID FK
- portfolio_id UUID FK
- security_id UUID FK
- state TEXT
- thesis_state TEXT
- deterioration_flags JSONB
- evidence_ids JSONB
- limitations JSONB

### portfolio_heat_results
- id UUID PK
- analysis_run_id UUID FK
- portfolio_id UUID FK
- heat_state TEXT
- sector_exposure JSONB
- factor_exposure JSONB
- cyclicality_exposure JSONB
- concentration JSONB
- limitations JSONB

### exitability_results
- id UUID PK
- analysis_run_id UUID FK
- portfolio_id UUID FK
- security_id UUID FK
- position_value NUMERIC NULL
- exitability_state TEXT
- expected_exit_days NUMERIC NULL
- turnover_context JSONB
- stress_context JSONB
- evidence_ids JSONB
- limitations JSONB

### rotation_reviews
- id UUID PK
- analysis_run_id UUID FK
- portfolio_id UUID FK
- incumbent_security_id UUID
- candidate_security_id UUID NULL
- outcome TEXT
- incumbent_context JSONB
- candidate_context JSONB
- transition_cost_context JSONB
- comparable_evidence_state TEXT
- limitations JSONB
- created_at TIMESTAMPTZ

Candidate_security_id may be null when the valid alternative is CASH_PREFERRED.

## 17. Watchlists

### watchlists
- id UUID PK
- user_id UUID FK
- name TEXT
- created_at / updated_at

### watchlist_items
- watchlist_id UUID FK
- security_id UUID FK
- strategy_archetype_id TEXT NULL
- state TEXT
- thesis_note TEXT NULL
- added_at TIMESTAMPTZ
- PRIMARY KEY (watchlist_id, security_id)

### watch_observations
- id UUID PK
- watchlist_id UUID FK
- security_id UUID FK
- as_of TIMESTAMPTZ
- observation_state TEXT
- analysis_run_id UUID NULL
- change_summary JSONB

Watch does not imply executable signal authority.

## 18. Audit and version trace

### policy_versions
Optional registry snapshot:
- policy_type TEXT
- policy_id TEXT
- version TEXT
- knowledge_hash TEXT
- lifecycle TEXT
- effective_from TIMESTAMPTZ NULL
- metadata JSONB
- PRIMARY KEY (policy_type, policy_id, version)

### audit_events
- id UUID PK
- user_id UUID NULL
- analysis_run_id UUID NULL
- event_type TEXT
- entity_type TEXT
- entity_id TEXT NULL
- payload JSONB
- created_at TIMESTAMPTZ

Do not store access tokens, credentials or raw secrets in audit payloads.

## 19. Suggested logical foreign-key flow

```text
users
 ├─ portfolios ─ portfolio_positions
 ├─ watchlists ─ watchlist_items
 ├─ analysis_runs
 └─ universe_runs

securities
 ├─ market_bars
 ├─ financial_periods
 ├─ corporate_actions
 ├─ evidence_records
 ├─ diagnostic_results
 └─ strategy_evaluations

source_observations
      ↓
normalized evidence_records
      ↓
diagnostic_results
      ↓
score_results + gate_results
      ↓
strategy_evaluations
      ↓
strategy_confluence_results
      ↓
opportunity_context
      ↓
portfolio review / final response
```

## 20. Indexing priorities

Likely important indexes:

- market_bars(security_id, timeframe, bar_time)
- financial_periods(security_id, period_end, reported_at)
- source_observations(security_id, observation_type, effective_time)
- evidence_records(security_id, evidence_family, as_of)
- evidence_records(input_fingerprint, owner_tool_id, owner_tool_version)
- analysis_runs(user_id, created_at)
- diagnostic_results(analysis_run_id, diagnostic_id)
- strategy_evaluations(analysis_run_id, archetype_id)
- detector_results(universe_run_id, security_id, archetype_id)
- portfolio_positions(portfolio_id, security_id)
- watchlist_items(watchlist_id, security_id)

## 21. Retention and reproducibility

An analysis should be reproducible from:

- request/as-of context;
- security identity;
- source observation lineage;
- tool/computation versions;
- evidence fingerprints;
- diagnostic registry version;
- score policy version;
- gate policy version;
- strategy/archetype version;
- AI model/prompt version for qualitative findings.

Raw third-party payload retention should respect provider licensing and storage constraints.

## 22. Explicit non-schema authority

The database stores analytical state but does not create policy authority.

In particular, no row or status may by itself grant:

- BUY
- SELL
- TRIM
- ROTATE
- BROKER_ORDER

Those remain governed analytical/review concepts, with live broker-order authority out of scope.
