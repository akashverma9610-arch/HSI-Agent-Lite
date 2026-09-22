# Legacy HSI knowledge-extraction closure — Task #009

This closes the *knowledge extraction*, not the Lite product build. Sources
were read from clean, read-only `Hybrid-Stock-Intelligence` at
`f88b44d514fc9a2654040aa04e5350fc9e8660fe`; Lite began at
`a29d3dd6b846713e8f999c8614c0c850379e37ec`. Task #009
does not migrate a personal portfolio, transaction history, credentials,
screenshots, databases, or any broker/runtime capability. End SHAs and
working-tree status are verified again at task handoff.

| Major legacy knowledge area | Closure classification | Lite transfer / retained boundary |
| --- | --- | --- |
| Evidence/governance | EXTRACTED_WITH_LIMITATIONS | Task #004 governance artifacts; missing/conflicted evidence fails closed, real source coverage remains partial. |
| Source hierarchy | EXTRACTED | `governance/source_hierarchy.json`; source labels are not proof of primary authority. |
| PIT/history | EXTRACTED_WITH_LIMITATIONS | `governance/historical_pit.json`; complete owning-source known-at and strict replay coverage remain unproved. |
| 61 diagnostics | EXTRACTED_WITH_LIMITATIONS | Task #005 61 catalog records and evidence-dependency catalog; V2 definitions and operational coverage remain separate. |
| 10-point score | EXTRACTED | Task #006 score knowledge; incomplete mandatory inputs prevent a completed ranking. Score is not action authority. |
| Six gates | EXTRACTED_WITH_LIMITATIONS | Task #006 V1 gate catalog and successors; no FAIL override, V2 semantic approvals are not activation. |
| Strategy foundation | EXTRACTED_WITH_LIMITATIONS | Task #007 families/registry/geometry map; proposed product policies remain unavailable. |
| Strategy taxonomy relationship | EXTRACTED_WITH_LIMITATIONS | Task #008 35 archetypes, dependency and confluence maps; taxonomy does not activate strategies. |
| Portfolio | EXTRACTED_WITH_LIMITATIONS | State, accounting, health and heat contracts in `hsi_knowledge/portfolio/`; no owner-specific data or Lite runtime. |
| Rotation | EXTRACTED_WITH_LIMITATIONS | Comparable incumbent/candidate contract, cash alternative and friction/constraints retained; no automatic rotation. |
| Sell-side | EXTRACTED_WITH_LIMITATIONS | Approved-not-selected-not-active V1 vocabulary and fail-closed review boundary retained; no SELL/action producer. |
| Trim/profit taking | PROPOSED_NOT_ACTIVE | `TRIM_NOT_AUTHORIZED_V1`; trigger, quantity, tax and re-entry rules unavailable. |
| Market context | EXTRACTED_WITH_LIMITATIONS | Regime/sector/relative strength/macro-news already covered; one residual two-tail market-extremes contract added. No market-state trade action. |
| Liquidity/exitability | EXTRACTED_WITH_LIMITATIONS | Pool diagnostics distinguished from size-aware portfolio exitability; quantitative thresholds remain unresolved. |

The six-row [market-context closure map](../hsi_knowledge/portfolio/MARKET_CONTEXT_CLOSURE_MAP.json)
marks four areas `ALREADY_COVERED` and the downside/upside extremes
pair `EXTRACTED_RESIDUAL` through one narrow artifact. “Sufficient for
future runtime design” in that map means knowledge scope, not live source
readiness or permission to deploy.

## Explicitly retained unavailable or unresolved work

- Live/prospective source quality, PIT history and historical replay are not
  closed merely by a documented contract.
- Strategy-specific long-term, Event/Catalyst, Tactical, Fast-Rotation and
  Profit-Harvesting product policies are not selected/active where the
  Task #002 authority map marks them proposed.
- Sell-side approval did not select/activate an action producer. Trim trigger,
  quantity, tax and re-entry remain `UNAVAILABLE`.
- Gate 1 V2 parcel/horizon inputs, comparable forward economics, future cash
  settlement and size-aware exitability need separately governed sources.
- Market extremes thresholds and factor coverage require calibration; euphoria
  is not a top or sell rule, and crisis is not a sell-all instruction.
- Entry/stop/target geometry differs by strategy; generic price-structure
  Rule 46 is not universal fundamental or catalyst invalidation.
- No portfolio engine, sell/rotation engine, data provider, database, agent,
  RAG, API, UI, notification or broker implementation was transferred.

## Independence decision

`YES_WITH_RECORDED_LIMITATIONS` — Lite now has a pinned, machine-readable
knowledge basis for future design across the requested legacy domains. It
does **not** have an operational investing system, active sell/trim policy,
production calibration or permission to trade. Future implementation must
resolve the listed blockers under Lite's own governance; ordinary development
need not keep the old repository as an ongoing design dependency. The old
HSI's intended future role is
`ARCHIVED_READ_ONLY_PROVENANCE_REFERENCE`: preserved, not deleted or
rewritten, no runtime dependency, no ordinary development dependency, and
source review only when explicitly required. This sentence documents a
future role; Task #009 does **not** archive or modify that repository.
