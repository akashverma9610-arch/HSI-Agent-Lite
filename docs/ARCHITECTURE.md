# Architecture

```text
USER / SENSEEDGE LITE
        |
        v
MASTER HSI ORCHESTRATOR
        |
  +-----+------------------------+
  |              |              |
  v              v              v
LIVE DATA     HSI RAG       PORTFOLIO DB
TOOLS         KNOWLEDGE
  |
  +--> Technical Tool
  +--> Fundamental Tool
  +--> Market/Regime Tool
  +--> Liquidity Tool
  +--> Resilience Tool
  +--> News/Catalyst Agent
        |
        v
NORMALIZED EVIDENCE REGISTRY
        |
        v
61-DIAGNOSTIC RECONCILIATION
        |
        +--> 10-POINT SCORE
        |
        +--> SIX EXECUTION GATES
        |
        v
STRATEGY MATCHER
        |
        v
FINAL HSI SYNTHESIS
```

The legacy HSI repo is an external read-only specification source, never a runtime dependency.
