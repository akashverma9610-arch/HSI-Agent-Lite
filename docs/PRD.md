# PRD — HSI Agent Lite

## 1. Product scope

HSI Agent Lite is a private, invite-only Indian-equity research and portfolio-intelligence system for the owner and approximately 10–12 trusted users. It must support whole-NSE discovery, stock analysis, Watch, portfolio review and explainable strategy matching without live broker-order authority.

The product is deliberately hybrid:

- deterministic code/tools calculate facts, indicators and reusable evidence;
- governed knowledge defines diagnostics, score, gates, strategy semantics and lifecycle;
- AI agents investigate qualitative questions and synthesize conclusions;
- humans retain final decision authority.

Core law: **calculate once → normalize once → reuse everywhere**.

## 2. Primary product surfaces

### Home
Portfolio/Watch summary, market/regime context, data-quality warnings, recent material research changes and pending reviews.

### Scan
Whole-NSE staged discovery. Cheap deterministic filters and strategy detectors must run before expensive deep research. A security may match multiple strategy archetypes.

### Analyse
Single-stock deep analysis with strategy-specific evidence collection and explainable output.

### Watch
Watch-only monitoring of selected candidates, thesis changes, catalyst changes, entry readiness and deterioration. No automatic order placement.

### Portfolio
Holding health, portfolio heat, concentration, exitability, thesis deterioration, rotation comparison and profit-review state. A portfolio analytical state is not trade authority.

## 3. Required analysis outputs

A stock-analysis response should be able to show, when supported:

- canonical company/symbol identity;
- data timestamps, freshness and source quality;
- normalized technical, fundamental, market, sector, liquidity and event evidence;
- 61-diagnostic reconciliation;
- global HSI 0–10 score and completeness state;
- six execution-gate states;
- matched strategy archetypes and family;
- Strategy Confluence with overlap/correlation guard;
- business/fundamental thesis;
- news/catalyst and “Why Now?” context;
- technical timing;
- valuation;
- risk flags and limitations;
- liquidity/exitability;
- Entry / SL / T1 / T2 / Extended visual inputs where an approved strategy-specific geometry policy exists;
- thesis and invalidation;
- portfolio-fit context;
- provenance/citations;
- explicit UNKNOWN / UNAVAILABLE / NON_EVALUABLE states where evidence is insufficient.

## 4. Whole-NSE discovery requirement

The system must not deep-analyse the entire NSE universe with AI.

Target product flow:

Whole NSE → data quality → investability → red-flag screen → cheap strategy detectors → candidate union → preliminary validation → deep HSI analysis → strategy confluence → Why Now → technical timing → regime compatibility → risk/reward → portfolio fit → delivery bucket.

Discovery gates are separate from the existing six execution gates.

The scan must support configurable universes, including user-configurable market-cap bands rather than one hard-coded band.

## 5. Strategy model

The initial taxonomy contains 35 strategy archetypes grouped into six primary families:

- Business / Earnings
- Price / Flow
- Recovery / Re-Rating
- Industry / Cycle
- Catalyst
- Structural Growth

Each archetype consumes only relevant evidence. The system must not force every stock through every component equally.

Future strategies and versions must be addable through registry/configuration and governed evidence dependencies without redesigning the technical/fundamental engines.

## 6. Tool-backed product capabilities

The product requires reusable backend tool families. These are not independent AI agents.

### Identity and source integrity
- Security Identity Tool
- Source Reliability / Freshness Tool
- PIT / Historical Guard
- Corporate Action Tool

### Market and technical
- Price & Market Data Tool
- Technical Indicator Tool
- Market Structure Tool
- Relative Strength Tool
- Volume / Flow Tool
- Liquidity Structure Tool
- Sector Tool
- Market Regime / Market Extremes Tool

### Fundamental and research
- Fundamental Financial Tool
- Financial Comparability Tool
- Earnings Momentum Tool
- Valuation Tool
- Catalyst/Event Data Tool

### Discovery
- Universe Tool
- Data Quality Screener
- Investability Screener
- Red-Flag Screener
- Strategy Detector Framework
- Candidate Union Tool
- Strategy Confluence Tool

### Action-context / geometry
- Entry Geometry Tool
- Stop / Invalidation Tool
- Target / Scenario Tool
- Risk / Reward Tool

### Portfolio
- Portfolio State Tool
- Portfolio Heat Tool
- Exitability Tool
- Rotation Comparison Tool
- Holding Health Tool

Logical tools may share one deployable subsystem; the product must not require dozens of microservices.

## 7. AI agent requirements

Initial AI agent count is intentionally limited to three.

### Master HSI Agent
Orchestrates user intent, requests governed tools/evidence, reconciles strategy context, score, gates and portfolio context, and produces the final explainable response.

### News / Catalyst Research Agent
Investigates announcements, filings, news, policy events, event identity, novelty, materiality and company transmission. It must consume clean event/source records and must not manufacture source facts.

### Deep Research Agent
Handles qualitative deep work such as business model, moat, TAM, competitors, management quality, guidance interpretation, forward scenarios and contextual valuation.

AI agents must not own deterministic calculations such as RSI, ROCE, RVOL, P/E, sector RS or position concentration.

## 8. Evidence and calculation ownership

Each deterministic metric family must have one calculation owner. Diagnostics, scores, gates, strategies and agents consume normalized evidence rather than recalculate the same metric independently.

Evidence must retain:

- identity/security;
- evidence type;
- as-of time;
- source and source timestamp;
- known-at/receipt/ingestion metadata where relevant;
- normalized payload;
- quality/freshness/conflict state;
- provenance;
- computation ID/version;
- runtime owner.

Missing evidence must remain UNKNOWN/UNAVAILABLE rather than defaulting to PASS, zero or neutral.

## 9. Portfolio product requirements

Portfolio intelligence must support:

- positions and cash;
- holding health;
- thesis state;
- portfolio heat and concentration;
- sector/factor/cyclicality exposure;
- liquidity/exitability;
- comparable incumbent-versus-candidate rotation review;
- cash as a valid rotation alternative;
- analytical profit-review state.

Current governance retains `TRIM_NOT_AUTHORIZED_V1`. T1 achievement or euphoria alone must not authorize a trim.

No product surface may automatically place a broker order.

## 10. User-facing analytical states

The system should support delivery states such as:

- A_ACTIONABLE_NOW
- B_ENTRY_WATCH
- C_RESEARCH_WATCH
- D_QUALITY_WRONG_PRICE
- E_REJECT_AVOID
- NON_EVALUABLE

These are analytical states, not execution commands.

## 11. Non-functional requirements

- invite-only authentication;
- owner/user portfolio isolation;
- auditable source and computation provenance;
- reproducible deterministic calculations;
- explicit model/strategy versions;
- fail-closed missing/conflicted evidence behavior;
- bounded AI cost through staged scanning;
- no secret/credential persistence in source control;
- provider-neutral data and LLM adapters;
- testable contracts;
- no live broker-order authority.

## 12. Product success criteria

A useful private pilot should be able to:

1. scan a configured NSE universe without deep-AI calls on every security;
2. identify strategy-specific candidates using reusable evidence;
3. deep-analyse finalists with explainable facts and AI interpretation clearly separated;
4. distinguish good company, good opportunity and good entry;
5. surface strategy confluence without double-counting correlated evidence;
6. compare new candidates with existing holdings using portfolio context;
7. remain useful when evidence is partial by reporting limitations rather than fabricating certainty.
