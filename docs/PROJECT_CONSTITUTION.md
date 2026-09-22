# HSI Agent Lite — Project Constitution

## Mission
Build a simpler private HSI implementation for the owner and approximately 10–12 trusted users using deterministic analytical tools, normalized evidence, 61-diagnostic reconciliation, a 10-point score, six execution gates, strategy matching, RAG knowledge, and a small number of AI agents.

## Legacy boundary
The existing `Hybrid-Stock-Intelligence` repository is immutable from this project.

Allowed: read approved/frozen diagnostic definitions, execution-gate rules, strategy rules/theses, evidence policies, source hierarchy, portfolio/rotation/profit-taking logic, and accepted governance lessons.

Forbidden: writing to the legacy repo, migrating its runtime DB, depending on unfinished modules, copying secrets/tokens/user data/runtime state, or silently changing approved rule meaning.

## Architectural laws
1. Calculate once.
2. AI interprets; code calculates.
3. RAG is knowledge, not market truth.
4. All engines/tools produce typed normalized evidence.
5. 61 diagnostics reconcile evidence; they do not duplicate technical/fundamental engines.
6. Gates outrank scores.
7. No live order authority.
8. Final investment action remains human.
9. Optimize for 10–12 trusted users.
10. Every material conclusion must have provenance.

## Change control
No new engine, agent, strategy, gate, or provider is added merely because an AI suggests it. Material additions require a scoped task and tests.
