# TASK #001 — HSI_AGENT_LITE_PROJECT_FOUNDATION

Create a NEW private repository. Do not modify `Hybrid-Stock-Intelligence`.

## Mandatory boundary
1. Legacy HSI is READ-ONLY.
2. No commit/branch/push/edit/migration/destructive command against it.
3. No credentials, `.env`, databases, tokens, user data, or runtime artifacts copied from it.
4. No stock-analysis functionality in TASK #001.
5. No live broker order execution.

## Repository
If GitHub CLI is authenticated:
`gh repo create HSI-Agent-Lite --private --source . --remote origin`

If it already exists, verify it is private.

## Required foundation
Retain/create the scaffold and documents from this bootstrap package.

## Core laws
- AI interprets; code calculates.
- RAG defines knowledge; live/timestamped sources define facts.
- Calculate once → normalize once → reuse everywhere.
- 61 diagnostics reconcile normalized evidence; do not duplicate specialist calculations.
- A failed critical gate cannot be overridden by score or LLM.
- Maximum initial AI agents: Master HSI, News/Catalyst Research, Deep Research.
- No live broker order authority.
- Optimize for owner + approximately 10–12 trusted users.

## Validation
Before commit:
- repo is private
- `.env` ignored
- no secrets
- legacy repo unchanged
- no functional analysis code

## Commit
`chore: establish HSI Agent Lite foundation`

## Return
Repository URL, commit SHA, file tree, validation results, explicit legacy-repo unchanged statement, blockers.

STOP after TASK #001. Do not start TASK #002.
