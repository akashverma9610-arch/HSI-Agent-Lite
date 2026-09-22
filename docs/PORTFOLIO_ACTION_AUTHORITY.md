# Portfolio analytical state versus action authority

Task #009 transfers policy knowledge only. The nine
`hsi_knowledge/portfolio/*.json` policy records have
`KNOWLEDGE_ONLY_REVIEW_REQUIRED` Lite lifecycle. There is no Lite portfolio
runtime, recommendation or order producer. In particular,
`broker_order_authority = false`.

| Layer | Examples | Meaning |
| --- | --- | --- |
| Analytical state | HEALTHY, REVIEW, DETERIORATING, THESIS_INVALIDATED, ROTATION_CANDIDATE, PROFIT_REVIEW | A point-in-time interpretation requiring provenance and strategy context. It may be unknown or contested. |
| Action vocabulary | HOLD, TRIM, EXIT, ROTATE, BUY, BROKER_ORDER | A future policy decision or external transaction. No state in this extraction grants it. |

Holding health, high/low global score, target T1, euphoria, price structure and
capital inefficiency are not automatic sell/trim/rotation rules. Applicable
six gates remain independent constraints. A FAIL cannot be overridden by
global score, strategy score, confluence, portfolio preference or AI
interpretation. Unknown inputs never become PASS.

Legacy sell-side V1 was **APPROVED, NOT SELECTED, NOT ACTIVE**; it defined
HOLD, EXIT_TO_CASH, ROTATE, REVIEW_REQUIRED and NO_ACTION vocabulary but no
selected action producer. The later sell/risk work was a research shadow.
`TRIM_NOT_AUTHORIZED_V1` remains explicit. Human review and a separately
governed activation decision would be required before any future action
policy; even then, broker authority would require its own authorization.

The 35 archetypes in [Task #008 taxonomy](STRATEGY_TAXONOMY_AND_CONFLUENCE.md)
are contextual: a compounder thesis, breakout condition, turnaround, or
Event/Catalyst case can have different evidence and invalidation. A global
score alone cannot authorize hold, trim, exit or rotation. Task #007
[geometry authority](STRATEGY_FAMILY_EXTRACTION.md) likewise keeps
strategy-specific entry/stop/target definitions distinct.
