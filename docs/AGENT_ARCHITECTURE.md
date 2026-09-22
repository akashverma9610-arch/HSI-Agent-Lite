# Agent Architecture

## Master HSI Agent
Understands intent, chooses tools/research, retrieves relevant HSI knowledge, requests normalized evidence, invokes diagnostics/gates/strategies, and synthesizes the result.

Forbidden: inventing missing numerical data, overriding failed gates, changing strategy rules, or placing broker orders.

## News/Catalyst Research Agent
Prioritizes exchange filings, company disclosures, and primary sources; deduplicates and returns event, materiality, direction, horizon, timestamps, and citations.

## Deep Research Agent
Used only for difficult/ambiguous finalist cases.

## Budget rule
Do not invoke an agent when deterministic code can answer.
