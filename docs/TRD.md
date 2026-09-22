# TRD — HSI Agent Lite

## Initial stack
Python 3.12+, FastAPI, PostgreSQL, SQLAlchemy/Alembic, managed identity using PKCE/RS256, one vector store selected later, LLM provider abstraction, optional Lyzr orchestration, frontend choice deferred.

## Pipeline
User request → orchestrator → deterministic tools → optional research agent → normalized evidence → 61 diagnostics → 10-point score → six gates → strategy matcher → final LLM synthesis → response with provenance.

## AI agents
Maximum initial agents:
1. Master HSI Agent
2. News/Catalyst Research Agent
3. Deep Research Agent

Do not create AI agents for deterministic calculations.
