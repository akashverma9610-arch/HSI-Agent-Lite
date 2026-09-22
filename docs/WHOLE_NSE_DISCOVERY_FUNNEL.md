# Whole-NSE discovery funnel — Task #010 contract

This is a frozen **design contract**, not a scanner or investment service.
It starts from a point-in-time canonical NSE security universe of whatever
size exists, rather than a fixed list of 1,500 or 2,200 securities. No
provider, downloader, calculation worker, LLM, RAG, API, UI, database, or
broker connection is implemented.

## Why stages and costs matter

Running full company, news and AI research on every listed security would
multiply expensive requests and often spend them on stale, uninvestable or
obviously mismatched names. The contract therefore uses these cost classes:

| Class | Intended use |
| --- | --- |
| `C0_METADATA` | Identity, listing, filing timestamps, source/quality flags. |
| `C1_CHEAP_DETERMINISTIC` | Shared price/volume and simple investability facts. |
| `C2_MODERATE_DETERMINISTIC` | Strategy-specific cheap probes and preliminary validation on the investable subset. |
| `C3_DEEP_STRUCTURED_RESEARCH` | Long-form, strategy-selective company research on validated finalists only. |
| `C4_AI_DEEP_RESEARCH` | Optional future AI work on finalists, separately approved and budgeted; disabled by default. |

No fixed candidate count or numeric market-cap, liquidity, R:R or bucket
threshold is selected here. Budgets are *stage permissions*: C3/C4 cannot
run over the whole universe, and C4 is never required for a cheap detector.
This reduces API/data/AI cost without turning missing data into rejection.

| Order | Stage | Main output / cost boundary |
| ---: | --- | --- |
| 0 | Whole NSE universe | Canonical PIT security identities; C0. |
| 1 | Discovery Gate 0 — data quality | Evaluable, limited, insufficient, conflicted or non-evaluable; C0/C1. |
| 2 | Discovery Gate 1 — investability | Configurable universe and cheap turnover/status filters; C0/C1. |
| 3 | Discovery Gate 2 — red flags | Verified universal concerns versus strategy-relative risks; C0/C1. |
| 4 | Cheap strategy detectors | Possible-fit probes for all 35 archetypes; C0–C2, no AI. |
| 5 | Candidate union/deduplication | One security identity, multiple strategy triggers and shared evidence IDs; C1. |
| 6 | Preliminary strategy validation | Source, consistency, flags, preliminary valuation/exitability; C0–C2. |
| 7 | Deep HSI analysis | Only relevant fundamental, business, management, forward and valuation modules for finalists; C3, optional approved C4. |
| 8 | Strategy confluence | Task #008 evidence/dependency confluence, not detector-count voting; C2. |
| 9 | Catalyst / WHY_NOW | Strategy-relative company transmission and timing; C3 where applicable. |
| 10 | Technical timing | Company quality and current entry are separate; C2. |
| 11 | Regime compatibility | Contextual risk-on/risk-off fit; C2. |
| 12 | Risk / reward | Current strategy-specific geometry and friction; C2. |
| 13 | Portfolio fit | Task #009 heat, concentration, exitability, thesis overlap and cash; C2. |
| 14 | Final delivery bucket | Analytical state only, never an order; C1. |

The machine order and class limits are in
[WHOLE_NSE_FUNNEL.json](../hsi_knowledge/discovery/WHOLE_NSE_FUNNEL.json).
The gate contracts are separate files in that directory.

## Discovery gates are not execution gates

Discovery Gates **0–2** ask whether a security can continue through
research: data quality, configurable investability and red flags. They do
not assign the 10-point score to bad data. Critical missing/conflicted
inputs yield `NON_EVALUABLE` or an explicit limitation; an unknown is not
zero, PASS or an investment failure.

The existing **Execution Gates 1–6** in
[the Task #006 catalog](../hsi_knowledge/gates/index.json) ask whether a
separately qualified action is admissible under governed constraints.
Discovery Gate 0/1/2 **≠** Execution Gate 1–6. No execution-gate FAIL
can be overridden by a discovery result, global score, strategy score,
confluence, portfolio preference or AI.

Gate 1 permits user-configured `MICRO`, `SMALL_MID`, `MID_LARGE`,
`ALL_NSE` or `CUSTOM` presets with no numeric bounds selected here;
the founder's often-mentioned ₹3,000–30,000 crore scan is not mandatory.
Actual position-size-aware exitability or days-to-exit is deferred until
a position and valid turnover evidence exist; it is not cheaply asserted
for every security. Gate 2 reserves truly universal severe, verified
hazards for universal treatment. High leverage may be adverse to a
compounder yet central to a deleveraging thesis. Weak margins may support
recovery; blanket negative-metric rejection is prohibited. A cheap auditor
or governance flag requests materiality review; size-aware exitability is
likewise deferred, never presumed from a whole-universe metadata pass.

## Shared primitives and 35 possible-fit detectors

The [primitive catalog](../hsi_knowledge/discovery/DETECTOR_PRIMITIVE_CATALOG.json)
defines one future canonical owner for each cheap fact. Existing Task #005
evidence families and diagnostic IDs are referenced where available;
missing source contracts are explicitly marked future-defined. Detectors
reuse primitive IDs, not independent calculation copies.

The [detector catalog](../hsi_knowledge/discovery/STRATEGY_DETECTOR_CATALOG.json)
has one record for each Task #008 archetype. Each records its inexpensive
dependencies, diagnostic references, trigger semantics, missing-input
behavior, false-positive tolerance, cost and escalation destination.
Fundamental Inflection can probe comparable growth/margin/return trends;
Pre-Breakout can probe base/contraction/relative strength; Market-Red
Resilience needs repeated weak-market comparisons. Institutional
Accumulation uses only observable price/volume, delivery if available and
RS/accumulation *proxies*: it never identifies institutional buyers.
An event-centered archetype with no cheap public event evidence remains
deferred; it does not force a C3/C4 whole-universe crawl.

A detector means “worth a closer look,” not “approved investment.”
High false-positive tolerance at this cheap stage is intentional;
preliminary validation removes obvious mismatches before deep spend.

## Union, validation and deep analysis

One security can trigger several detectors. The
[candidate union](../hsi_knowledge/discovery/CANDIDATE_UNION_CONTRACT.json)
merges by canonical identity and as-of cutoff while retaining every
archetype trigger, detector version, evidence ID, observed/known-at time
and source lineage. Shared evidence is referenced once, not duplicated
per strategy. Detector count is not strategy confluence.

[Preliminary validation](../hsi_knowledge/discovery/PRELIMINARY_VALIDATION_CONTRACT.json)
checks current sources, strategy requirements, red flags, relevant
preliminary valuation, investability and consistency without deep
business/news analysis. Only validated finalists reach the
[deep module map](../hsi_knowledge/discovery/DEEP_ANALYSIS_MODULE_MAP.json).
Modules cover fundamentals, business, management, forward scenarios and
valuation. Selection follows the archetype dependency matrix; a technical
setup does not automatically request every business module, and one
financial fact is not recomputed for each triggered strategy.

Confluence then applies the existing Task #008
[model](../hsi_knowledge/strategies/STRATEGY_CONFLUENCE_MODEL.json):
independent evidence and conflicts matter, not the number of detectors
that happened to fire.

## Why-now, timing, regime, asymmetry and portfolio

`WHY_NOW` asks why a company-specific opportunity matters *now*:
commissioning, order execution, margin normalization, deleveraging,
product/customer additions, policy change or another evidenced catalyst.
Event presence alone is not impact. Catalyst relevance follows each
archetype's `CATALYST_NEWS` dependency; it is not a universal gate for
long-term strategies. A strong company without a current catalyst may
remain a long-term candidate.

Technical timing can say `GOOD_COMPANY_BAD_TIMING`, `EARLY_SETUP`,
`EXTENDED`, `STRUCTURE_INVALID` or `NOT_APPLICABLE`; good fundamentals
do not create a good entry. Regime compatibility distinguishes risk-off
quality/resilience/cash-flow preferences from risk-on emerging,
breakout/cyclical opportunities without inventing thresholds or BUY/SELL.
Its 35 archetype profiles are explicitly unvalidated semantic design
hypotheses, not active regime gates.
In short, `STOCK_QUALITY != CURRENT_OPPORTUNITY_QUALITY`.

R:R requires current entry, strategy-governed invalidation/stop, first and
later targets where valid, horizon and friction. Task #007
[geometry authority](../hsi_knowledge/strategies/GEOMETRY_AUTHORITY_MAP.json)
prevents a universal stop or target. No universal minimum R:R is selected:
good quality with poor current asymmetry can stay on Watch.

Portfolio fit uses Task #009's
[state, heat and rotation contracts](../hsi_knowledge/portfolio/README.md):
sector/factor/cyclical/market-cap exposure, correlation, exitability,
proposed weight, thesis overlap and cash. Stock strength does not ensure
portfolio suitability. Cash unknown is not zero. This stage cannot mutate
a portfolio.

## Delivery is analytical, not execution

The buckets are `A_ACTIONABLE_NOW`, `B_ENTRY_WATCH`,
`C_RESEARCH_WATCH`, `D_QUALITY_WRONG_PRICE`, `E_REJECT_AVOID` and
`NON_EVALUABLE`. They distinguish current opportunity, entry waiting,
research gaps, wrong price, verified rejection and inability to assess.
`A_ACTIONABLE_NOW` is a *future semantic label* requiring all applicable
execution gates to be admissible; it is not produced by this design task
and has no broker-order authority. No bucket places an order.

Unresolved before runtime: provider/source and PIT contracts, preset
numbers, minimum history/liquidity and position-size exit calibration,
corporate-action reconciliation, future primitive owners and evidence
sources, strategy-specific trigger validation, C3/C4 budgets, catalyst
materiality, strategy geometry, regime and R:R calibration, portfolio
inputs, and independent approval/activation of any delivery consumer.
