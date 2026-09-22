# Test Strategy

Required:
1. deterministic unit tests
2. evidence schema tests
3. diagnostic mapping tests
4. score/gate tests
5. strategy eligibility tests
6. agent structured-output contract tests
7. RAG retrieval tests
8. API tests
9. auth/user-isolation tests
10. end-to-end frozen-fixture analysis tests

Critical invariants:
- same metric is not authoritatively recomputed in multiple places
- failed critical gate cannot be overridden by score/LLM
- missing evidence never becomes hallucinated PASS
- legacy repo is never mutated
- no broker order path exists
