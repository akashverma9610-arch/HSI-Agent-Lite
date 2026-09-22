# TRD — HSI Agent Lite

## 1. Technical objective

Implement HSI Agent Lite as a modular Python backend in which deterministic tools own calculations, normalized evidence is the shared internal contract, governed knowledge defines policy semantics, and a small AI-agent layer performs qualitative research and final synthesis.

Primary implementation law: **AI interprets; code calculates.**

## 2. Initial stack

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy + Alembic
- managed identity with Authorization Code + PKCE / RS256
- provider-neutral market/fundamental/event adapters
- vector store selected later (pgvector or Qdrant acceptable candidates)
- provider-neutral LLM abstraction
- optional orchestration framework only if it reduces code complexity
- frontend implementation deferred from backend contracts

The private pilot target is approximately 10–12 trusted users, not enterprise-scale SaaS.

## 3. Runtime architecture

```text
User / UI
   ↓
API / Auth / Request Context
   ↓
Master HSI Orchestrator
   ├─ Tool Layer
   │   ├─ Identity & Source Integrity
   │   ├─ Market / Technical
   │   ├─ Fundamental / Valuation
   │   ├─ Sector / Regime / Liquidity
   │   ├─ Discovery
   │   ├─ Geometry / Risk
   │   └─ Portfolio
   ├─ Knowledge Resolver
   ├─ News/Catalyst Agent
   └─ Deep Research Agent
          ↓
Normalized Evidence Registry
          ↓
61 Diagnostic Reconciliation
          ↓
Global 10-point Score + Six Execution Gates
          ↓
35-Archetype Strategy Evaluation
          ↓
Strategy Confluence / Why-Now / Timing / Portfolio Fit
          ↓
Master HSI Synthesis
          ↓
Explainable Response + Provenance
```

## 4. Tool layer

Logical tools are Python modules/services under a future structure such as:

```text
app/
  tools/
    identity/
    source_quality/
    market_data/
    technical/
    fundamental/
    sector/
    regime/
    liquidity/
    valuation/
    catalyst/
    discovery/
    geometry/
    risk_reward/
    portfolio/
```

They need not be separate processes or microservices.

### 4.1 Identity & source-integrity tools

**Security Identity Tool**
Canonical symbol/security identity, ISIN/listing mapping, symbol changes and identity conflicts.

**Source Reliability Tool**
Source tier, timestamp, freshness, conflict state and provenance eligibility.

**PIT / Historical Guard**
Known-at/publication/receipt/effective-time checks for replay and historical analysis.

**Corporate Action Tool**
Split/bonus/rights and identity/price-basis adjustment context.

### 4.2 Market / technical tools

**Price & Market Data Tool**
Normalized OHLCV/delivery/trading-status observations.

**Technical Indicator Tool**
Single-owner calculation of reusable indicators such as SMA/EMA, RSI, ADX, ATR, OBV, RVOL and Ichimoku components.

**Market Structure Tool**
HH/HL-LH/LL, base, breakout, pullback, retest, compression and structural invalidation evidence.

**Relative Strength Tool**
Stock vs benchmark, sector and peer relative-strength evidence.

**Volume / Flow Tool**
Volume expansion/contraction, close-quality, up/down-volume asymmetry and accumulation/distribution proxies. It must not assert institutional identity.

**Liquidity Structure Tool**
Price/volume liquidity pools, sweeps, reclaim, stop-cluster proxies and related technical structure; not portfolio exitability.

**Sector Tool**
Sector mapping, sector trend, sector RS, breadth and leadership evidence.

**Market Regime / Extremes Tool**
Broad market regime plus separately governed downside-crisis and upside-euphoria context.

### 4.3 Fundamental / valuation tools

**Fundamental Financial Tool**
Revenue/PAT/EPS growth, margins, ROCE/ROE, leverage, interest cover, CFO/FCF, working capital, dilution and quarterly acceleration.

**Financial Comparability Tool**
Period basis, consolidated/standalone scope, units, denominators, exceptional items and other comparability guards.

**Earnings Momentum Tool**
Reusable acceleration/deceleration evidence derived from normalized financial series.

**Valuation Tool**
P/E, EV/EBITDA, P/B where relevant, PEG, FCF yield, historical/peer/forward valuation evidence.

**Catalyst/Event Data Tool**
Canonical event identity, source, time, company, type, deduplication and known-at metadata. Qualitative materiality belongs to the Catalyst Agent.

### 4.4 Discovery tools

**Universe Tool**
Build configured NSE universes.

**Data Quality Screener**
Cheap evaluability checks; missing/conflicted data produces NON_EVALUABLE-style states, not low scores.

**Investability Screener**
Market cap, trading status, liquidity, free float where reliable, turnover and exitability-oriented context.

**Red-Flag Screener**
Separates universal red flags from strategy-relative red flags.

**Strategy Detector Framework**
One reusable framework driven by 35 archetype detector definitions, not 35 duplicated engines.

**Candidate Union Tool**
Merge detector hits by canonical security identity while retaining trigger lineage.

**Strategy Confluence Tool**
Evaluate cross-strategy relationships with evidence/event/diagnostic overlap guards.

### 4.5 Geometry and risk tools

**Entry Geometry Tool**
Strategy-specific entry geometry only when selected policy authority exists.

**Stop / Invalidation Tool**
Price/structural, fundamental, catalyst, governance and strategy-specific invalidation remain distinct.

**Target / Scenario Tool**
T1/T2/Extended or scenario outputs only where supported by the selected strategy/policy.

**Risk / Reward Tool**
Entry-stop-target asymmetry and friction-aware risk/reward evidence.

### 4.6 Portfolio tools

**Portfolio State Tool**
Holdings, quantity, average cost, cash and derived values.

**Portfolio Heat Tool**
Sector/factor/cyclicality/concentration context.

**Exitability Tool**
Actual position-size-aware exitability using traded value/volume, float/stress/friction inputs; separate from liquidity-pool evidence.

**Rotation Comparison Tool**
Comparable incumbent-vs-candidate analysis with friction, taxes, horizon, portfolio fit and cash alternative.

**Holding Health Tool**
Current thesis/evidence/deterioration/review state.

## 5. Calculation ownership

One deterministic calculation family must have one authoritative runtime owner.

The normalized evidence registry is the sharing boundary. A consumer must reference evidence IDs/computation versions instead of re-running another subsystem's calculation.

Examples:

- Ichimoku calculated once → D12/D13/D14 and relevant strategies consume it.
- Base-pattern evidence calculated once → multiple setup/target consumers reuse it.
- Quarterly-growth evidence calculated once → score/diagnostics/strategies reuse it.
- Relative-strength evidence calculated once → D06, sector leader, resilience and pre-breakout consumers reuse it.

No LLM is a deterministic calculation owner.

## 6. Evidence contract

Each runtime evidence record should carry at minimum:

- evidence_record_id
- security_id
- evidence_type / family
- as_of
- source_id
- source_timestamp
- publication_time / receipt_time / effective_time where applicable
- payload
- quality_state
- freshness_state
- conflict_state
- provenance
- computation_id
- computation_version
- owner_tool
- created_at

Evidence lifecycle must support VALID, STALE, CONFLICTED, MISSING/UNKNOWN and equivalent governed states.

## 7. Diagnostic / scoring / gate runtime boundaries

### Diagnostics
61 diagnostics reconcile normalized evidence. They do not become new calculation engines.

### Global score
The accepted 0–10 score is deterministic once admitted diagnostic states are available. Mandatory missing inputs keep the final score incomplete/null. Optional inputs do not cause weight renormalization.

### Six execution gates
Six V1 gates remain separate blocking admissibility constraints. Gate FAIL/UNKNOWN behavior cannot be overridden by score or LLM.

Discovery Gate 0/1/2 are separate scan-funnel controls and must not reuse execution-gate IDs.

## 8. Strategy runtime design

The 35 archetypes are configuration/knowledge-driven consumers.

A future strategy evaluator should load:

- archetype version;
- required/optional/context evidence;
- diagnostic dependencies;
- horizon authority;
- geometry authority;
- gate applicability;
- lifecycle/activation state.

Unknown, proposed-only or unapproved strategy versions fail closed as STRATEGY_UNAVAILABLE.

Strategy Confluence must account for evidence/event/diagnostic overlap and must not equal naive match count.

## 9. AI agents

Maximum initial AI agents:

1. **Master HSI Agent**
2. **News/Catalyst Research Agent**
3. **Deep Research Agent**

The Master agent orchestrates; it does not bypass deterministic owners or gates.

Agents may:
- interpret qualitative evidence;
- request approved tools;
- summarize findings;
- formulate supported scenarios;
- reconcile conflicting qualitative claims;
- produce explainable synthesis.

Agents may not:
- silently calculate deterministic metrics in place of the tool owner;
- fabricate missing evidence;
- activate a strategy/model version;
- override a failed gate;
- place broker orders.

## 10. Whole-NSE compute strategy

Use cost classes to restrict expensive work:

- C0 metadata
- C1 cheap deterministic
- C2 moderate deterministic
- C3 deep structured research
- C4 AI deep research

C3/C4 work is allowed only after cheap discovery reduction unless explicitly requested for one stock.

The detector framework should use shared primitives and cached normalized evidence to avoid N × strategy × recalculation explosion.

## 11. Persistence boundaries

PostgreSQL is the system of record for runtime state, user portfolios, evidence metadata, analysis runs, outputs and audit references.

Large/raw provider payloads may be stored separately if needed, while relational tables retain canonical pointers, hashes and provenance.

Knowledge JSON under `hsi_knowledge/` remains version-controlled policy/configuration; it is not the mutable user/runtime database.

## 12. Provider abstraction

Define interfaces rather than binding core logic to a single provider:

- SecurityMasterProvider
- MarketDataProvider
- FundamentalDataProvider
- CorporateActionProvider
- NewsEventProvider
- SectorBenchmarkProvider

Provider responses must be normalized before entering the evidence registry.

## 13. Caching and idempotency

Deterministic tool outputs should be cacheable by:

`security_id + as_of + computation_id + computation_version + input_fingerprint`

Repeated consumers should reuse the same evidence record when inputs/version match.

Analysis runs require request/run IDs for reproducibility and audit.

## 14. Security and isolation

- bearer tokens validated server-side;
- owner/user portfolio records scoped by authenticated subject;
- secrets outside source control;
- provider credentials stored in secret manager/OS secure store;
- no arbitrary user-supplied JWT role trust;
- no broker-order capability in initial runtime.

## 15. Failure behavior

Fail closed where evidence or policy authority is required.

Examples:

- bad identity → NON_EVALUABLE;
- mandatory score input unavailable → score incomplete/null;
- strategy version unavailable → STRATEGY_UNAVAILABLE;
- gate UNKNOWN where policy says BLOCK → blocked;
- missing exitability inputs → UNKNOWN, not SAFE;
- missing source provenance → evidence inadmissible where required.

## 16. Testing

Required test families:

- tool calculation unit tests;
- provider normalization tests;
- evidence schema/provenance tests;
- calculate-once owner uniqueness tests;
- diagnostic reconciliation tests;
- score completeness tests;
- gate non-override tests;
- strategy-registry and detector tests;
- confluence overlap tests;
- portfolio isolation tests;
- PIT/lookahead tests;
- end-to-end deterministic replay tests.

## 17. Non-goals

Initial HSI Agent Lite does not require:

- dozens of autonomous agents;
- microservice-per-tool deployment;
- automatic model self-modification;
- live broker order placement;
- public multi-tenant SaaS billing;
- full-universe C4 AI research on every scan.
