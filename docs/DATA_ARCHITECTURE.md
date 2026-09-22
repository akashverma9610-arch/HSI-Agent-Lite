# Data Architecture

Evidence classes: PRICE, TECHNICAL, FUNDAMENTAL, MARKET, SECTOR, NEWS_EVENT, LIQUIDITY, RESILIENCE, PORTFOLIO, SOURCE_QUALITY.

Each evidence record includes: evidence_id, symbol, evidence_type, as_of, source, source_timestamp, payload, quality, freshness, provenance, computation_version.

Downstream components consume evidence records and do not independently recalculate the same metric without an explicit owner.
