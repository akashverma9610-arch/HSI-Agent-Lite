# HSI Compact Evidence Brain — implementation specification

Status: product requirements confirmed by owner; implementation details proposed for review. 24 September 2026.

## Objective and scope

Build HSI Agent Lite for the owner first, with boundaries that can support later scaling. The Brain preserves approximately ten years of available history for companies currently listed in the NSE universe as compact, traceable evidence and intelligence. It does not retain every PDF, page, text chunk, or AI intermediate. The source documents remain at exchange/company URLs. Missing historical coverage is explicit and never reconstructed by guesswork.

The system covers whole-NSE discovery at 09:16, 10:00, 13:00, and 15:29 IST on market days; live monitoring of holdings and selected candidates through Dhan; on-demand company research; portfolio comparison; and relevant NSE/BSE filings, Indian/global news, and macro events as they arrive. Web and Android are both first-version surfaces. It sends analytical alerts and Android push, but never places orders. Self-improvement is out of scope.

## What persists

1. **Company identity:** stable security identifier, ISIN, NSE/BSE symbols and effective dates, current listing status. Symbols are aliases, not primary keys.
2. **Annual/quarterly facts:** only reusable financial and operating values required by strategy dependencies: period and reporting scope, units, value, observation and publication/known-at times, source URL, page/table/section, extraction version and quality state. Examples include revenue, margins, earnings, cash flows, debt, returns, share count and segment values when relevant.
3. **Material events:** result, order, capacity, acquisition, management, governance and policy events; entity, event time, known-at time, cited source, affected metrics and supersession relation.
4. **Derived evidence:** deterministic trends such as multi-year growth, margin persistence, cash conversion or debt trajectory, each linked to input fact IDs, code/policy version and calculation time.
5. **Intelligence:** concise, dated business-history and catalyst interpretations, competing explanations, uncertainty and invalidation conditions. Interpretations link to facts/events; they are never promoted to raw facts.
6. **Strategy assessments:** 35 archetypes each return MATCH, NO_MATCH or INSUFFICIENT_EVIDENCE, with evidence IDs and independent-evidence overlap. Each valid strategy setup has its own geometry; otherwise it remains Research with no invented entry, stop or target.
7. **Portfolio state:** user-confirmed screenshot extraction, cash, holding-role suggestion, 0–100 target and actual risk score, explanation and proposed cash/rotation alternatives. Preserve the exact user-confirmed version of each snapshot.

No original PDFs, wholesale document embeddings or unreferenced prose are permanent Brain records. A short-lived processing copy may be needed for parsing, with a bounded cleanup rule to be defined during implementation. Source links may disappear; record content hashes and small permitted supporting snippets or table coordinates where possible, subject to source rights.

## Evidence record minimum

`evidence_id`, `security_id`, `kind`, `value_or_claim`, `unit`, `period_start`, `period_end`, `reporting_basis`, `source_publisher`, `source_url`, `source_locator`, `published_at`, `known_at`, `retrieved_at`, `extracted_at`, `status`, `extraction_version`, `source_hash`, `supersedes_id`, `input_evidence_ids`.

Status includes VERIFIED, UNVERIFIED, CONFLICTED, SUPERSEDED and UNAVAILABLE. Store ambiguous/conflicting extracts with their source IDs, but do not let them satisfy a mandatory strategy condition as confirmed facts. Preserve both sides of a conflict. A missing field is null with a reason, never zero.

## Processing and updates

Source discovery -> deduplicate document/event identity -> resolve company and reporting period -> extract candidate facts with page/section citations -> validate units, scope and arithmetic -> compare independent sources -> write immutable evidence version -> recompute only affected diagnostics/trends -> refresh only affected intelligence and strategy assessments -> assess portfolio impact -> emit a deduplicated alert when material.

NSE/BSE duplicates must point to one canonical event while retaining both source observations. A restated financial result supersedes the old value; historical as-known-at queries still distinguish what was available at the earlier time. AI labels bullish/bearish/neutral and immediate/quarterly/long-term transmission as interpretations with evidence, affected sectors/stocks and uncertainty, not as facts or calibrated probabilities.

Ten-year backfill uses a coverage ledger by company, financial year, document class and source. Backfill first captures core annual series and material events, then fills dependency gaps relevant to the 35 archetypes. New filings are processed promptly with retry and reconciliation; source publication does not imply immediate detection or complete extraction. The four market scans use the latest *known-at* admissible snapshot and show source freshness.

## Storage and retrieval

PostgreSQL tables own identities, observations, facts, events, diagnostics, assessments, portfolio snapshots and lineage. Exact numeric/temporal/identity queries use structured indexes. Text retrieval searches concise event descriptions, intelligence and governed methodology, then resolves their canonical IDs. A vector index is optional and disposable: it is not the authoritative store and can be rebuilt. One shared calculation owner serves all strategies.

Keep workflow orchestration outside the calculation authority. Use scheduled/event jobs for ingestion, retries, reconciliation and notifications; Python services own normalization, computations, gates and API. Choose n8n/Windmill only after verifying integration/operation needs rather than embedding strategy math in flow nodes.

## Listing and deletion rule

Discovery covers currently listed eligible NSE securities. Delisted securities leave active discovery immediately. The owner requested deletion of evidence and decision history when a delisted security is not held; if it remains held, preserve the portfolio entry and necessary history until the holding is resolved. The exact delayed-deletion trigger and data-retention implications require an implementation decision before destructive automation.

## Reuse and acceptance

Old HSI accepted calculations and proofs carry forward within their recorded scope; validate changed interfaces and final integration. Stock Predator provides scanner and Expo UI reference, not authoritative source or universal setup geometry. HSI Agent Lite is the product repository.

Acceptance for a first end-to-end slice: one current listed security, a source-linked filing fact with timestamp and page reference, a stored price observation, one reused diagnostic, one archetype assessment, a Research/Watch/setup result with missing-data behavior, an on-demand web/Android view, and a trace from output to source. Then broaden to all archetypes and the universe, without claiming coverage for unevaluable names.

## Decisions intentionally open

- Official/authorized automated source routes and rights for the personal build and later users.
- Ten-year per-company coverage target and measured gaps; no claim of complete backfill yet.
- Liquidity minimum, position-specific exitability calibration and risk-score formula/thresholds.
- Alert materiality, retention period for temporary parsing copies, scheduler choice and operational budgets.
- Exact strategy geometry and 4-hour NSE session aggregation rules where existing authority is absent.

The earlier ₹1 crore/95% liquidity example is an unapproved calibration candidate, not a production rule.
