# HSI Lite knowledge schema

The canonical unit is a versioned knowledge artifact validated by `hsi_knowledge/schema/knowledge.schema.json`. Its `details` payload is validated by the matching type profile (`diagnostic`, `gate`, or `strategy` when applicable). An artifact is policy/definition, never a live fact. Timestamped facts use `evidence.schema.json`. RAG may retrieve explanatory knowledge, but cannot supply a market fact, evaluate a threshold, activate a policy, or authorize an order. AI interprets; code calculates.

| Type | Purpose | Deterministic conditions? |
| --- | --- | --- |
| `diagnostic` | PASS/CAUTION/FAIL/UNKNOWN reconciliation of normalized evidence | Only a reviewed, uniquely owned check; no upstream metric recomputation |
| `gate` | Fail-closed eligibility decision | Yes, from approved policy; FAIL is non-overridable |
| `strategy` | Governed setup and policy references | Yes, only in approved eligibility/entry/invalidation/target policies |
| `governance_policy` | Authority, review and activation controls | May contain deterministic process conditions, not market metrics |
| `portfolio_policy` | Portfolio constraints and decision authority | May contain reviewed deterministic constraints |
| `evidence_definition` | Meaning, source, shape and freshness of evidence | No calculation; may declare quality requirements |
| `calculation_definition` | Single metric computation owner and version | Yes, one owner per metric/version |
| `interpretation_guidance` | Explanatory/RAG-only reading of facts | No executable threshold or decision authority |

Knowledge does not embed current prices, observations, or inferred facts. A deterministic artifact declares `deterministic_computation: true` and a non-null `calculation_owner`. A pure consumer has no calculation owner and references evidence IDs. Composite checks may reconcile multiple records without duplicating their component calculations. All actual rule definitions, thresholds and activation selections remain future reviewed work; the schemas contain none.

The artifact envelope includes authority, Lite lifecycle, legacy lineage, extraction and human-review state. It references the diagnostic, gate or strategy profile when applicable, so those payloads are validated with the envelope; resolvers must use the local packaged schemas, never network fetching. `status` is the Lite lifecycle field; type profiles call the same field `lifecycle`. The schema blocks active/approved mismatches; a versioned registry must compare all envelope/profile status, authority, ID, version and evidence-dependency fields for equality on every transition. The other five types have an envelope now but are barred from approval/activation until reviewed type-specific payload contracts exist. Neither schema nor a score grants broker order authority.
