# Legacy HSI Reuse Policy

Source repository: `Hybrid-Stock-Intelligence`.

## Allowed
Approved/frozen diagnostic definitions, strategy rules/theses, six gates, scoring philosophy, evidence policies, source hierarchy, portfolio/rotation/profit-taking rules, accepted governance lessons.

## Forbidden
Writing to the legacy repository, copying secrets/runtime data, importing unfinished modules as dependencies, treating obsolete drafts as authoritative, or silently changing rule meaning.

## Extraction record
Each reused rule must record:
- legacy source path
- source version/commit when available
- extracted meaning
- Lite representation
- unresolved ambiguity
- acceptance status

Conflicts become `CONFLICT_REVIEW_REQUIRED`.
