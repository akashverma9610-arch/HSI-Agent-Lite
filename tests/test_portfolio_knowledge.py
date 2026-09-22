"""Task #009: static, knowledge-only portfolio extraction checks."""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / "hsi_knowledge" / "portfolio"
SCHEMAS = ROOT / "hsi_knowledge" / "schema"
DOCS = ROOT / "docs"
LEGACY_SHA = "f88b44d514fc9a2654040aa04e5350fc9e8660fe"
POLICIES = {
    "portfolio_state", "holding_health", "portfolio_heat", "rotation",
    "sell_side_review", "trim_profit_taking", "thesis_invalidation",
    "exitability", "market_extremes_residual",
}


@pytest.fixture(scope="module")
def records():
    return {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in PORTFOLIO.glob("*.json")
        if path.stem != "MARKET_CONTEXT_CLOSURE_MAP"
    }


@pytest.fixture(scope="module")
def market_map():
    return json.loads((PORTFOLIO / "MARKET_CONTEXT_CLOSURE_MAP.json").read_text(encoding="utf-8"))


def validator():
    schemas = [json.loads(path.read_text(encoding="utf-8"))
               for path in SCHEMAS.glob("*.schema.json")]
    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas
    )
    envelope = next(schema for schema in schemas if schema["$id"].endswith("/knowledge.schema.json"))
    return Draft202012Validator(envelope, registry=registry, format_checker=FormatChecker())


def test_all_portfolio_artifacts_validate(records):
    assert set(records) == POLICIES
    check = validator()
    for name, record in records.items():
        assert not list(check.iter_errors(record)), name
        assert record["details"]["policy_id"] == name


def test_no_artifact_has_broker_order_authority(records):
    assert all(r["details"]["action_authority"]["broker_order"] is False for r in records.values())


def test_health_does_not_authorize_sell(records):
    health = records["holding_health"]["details"]
    assert health["assertions"]["health_implies_sell"] is False
    assert health["action_authority"]["exit"] is False


def test_candidate_score_not_automatic_rotation(records):
    rotation = records["rotation"]["details"]
    assert rotation["assertions"]["higher_candidate_score_sufficient"] is False
    assert rotation["action_authority"]["rotate"] is False


def test_rotation_allows_cash(records):
    rotation = records["rotation"]["details"]
    assert rotation["assertions"]["cash_alternative_allowed"] is True
    assert "CASH_PREFERRED" in rotation["decision_states"]


def test_rotation_requires_comparable_evidence(records):
    rotation = records["rotation"]["details"]
    assert rotation["assertions"]["comparable_incumbent_candidate_evidence_required"] is True
    assert "INSUFFICIENT_COMPARABLE_EVIDENCE" in rotation["decision_states"]
    assert any("incumbent" in item and "candidate" in item for item in rotation["required_evidence"])


def test_trim_is_proposed_unavailable(records):
    trim = records["trim_profit_taking"]
    assert trim["authority_status"] == "PROPOSED_NOT_ACTIVE"
    assert trim["details"]["legacy_lifecycle"] == "PROPOSED_NOT_ACTIVE"
    assert "TRIM_NOT_AUTHORIZED_V1" in trim["details"]["decision_states"]
    assert trim["details"]["assertions"]["approved_active_legacy_trim_policy_exists"] is False


def test_t1_alone_never_trims(records):
    assert records["trim_profit_taking"]["details"]["assertions"]["t1_alone_authorizes_trim"] is False


def test_euphoria_alone_never_trims(records):
    assert records["trim_profit_taking"]["details"]["assertions"]["euphoria_alone_authorizes_trim"] is False
    assert records["market_extremes_residual"]["details"]["assertions"]["euphoria_proves_top"] is False


def test_price_stop_not_universal_thesis_invalidation(records):
    details = records["thesis_invalidation"]["details"]
    assert details["assertions"]["price_stop_universal_thesis_invalidation"] is False
    assert details["assertions"]["rule46_price_structure_only"] is True


def test_liquidity_pool_not_exitability(records):
    assert records["exitability"]["details"]["assertions"]["liquidity_pool_equals_position_exitability"] is False


def test_market_context_closure_does_not_duplicate(market_map):
    entries = market_map["entries"]
    assert len(entries) == 6
    assert len({item["domain"] for item in entries}) == 6
    assert sum(item["new_extraction_required"] for item in entries) == 2
    for item in entries:
        assert item["existing_lite_artifacts"]
        assert all((ROOT / path).is_file() for path in item["existing_lite_artifacts"])
        assert item["status"] == ("EXTRACTED_RESIDUAL" if item["new_extraction_required"] else "ALREADY_COVERED")
    assert {item["existing_lite_artifacts"][0] for item in entries if item["new_extraction_required"]} == {
        "hsi_knowledge/portfolio/market_extremes_residual.json"
    }


def test_diagnostic_references_resolve(records):
    diagnostic_ids = {
        json.loads(path.read_text(encoding="utf-8"))["id"]
        for path in (ROOT / "hsi_knowledge" / "diagnostics" / "catalog").glob("*.json")
    }
    for record in records.values():
        assert set(record["details"]["diagnostic_dependencies"]) <= diagnostic_ids


def test_strategy_and_archetype_references_resolve(records):
    strategy_ids = {
        json.loads(path.read_text(encoding="utf-8"))["id"]
        for path in (ROOT / "hsi_knowledge" / "strategies" / "catalog").glob("*.json")
    }
    archetype_ids = {
        json.loads(path.read_text(encoding="utf-8"))["strategy_archetype_id"]
        for path in (ROOT / "hsi_knowledge" / "strategies" / "taxonomy").glob("*.json")
    }
    for record in records.values():
        assert set(record["details"]["strategy_dependencies"]) <= strategy_ids | archetype_ids


def test_gate_references_resolve(records):
    gate_ids = {
        json.loads(path.read_text(encoding="utf-8"))["id"]
        for path in (ROOT / "hsi_knowledge" / "gates" / "catalog").glob("*.json")
    }
    for record in records.values():
        assert set(record["details"]["gate_dependencies"]) <= gate_ids


def test_action_authority_human_non_executable(records):
    for record in records.values():
        details = record["details"]
        assert record["status"] == "REVIEW_REQUIRED"
        assert details["human_review_required"] is True
        assert details["lite_lifecycle"] == "KNOWLEDGE_ONLY_REVIEW_REQUIRED"
        assert not any(details["action_authority"].values())
    assert "broker_order_authority = false" in (DOCS / "PORTFOLIO_ACTION_AUTHORITY.md").read_text(encoding="utf-8")


def test_no_personal_portfolio_data_in_artifacts(records, market_map):
    prohibited_keys = {
        "account_number", "broker_account", "user_id", "owner_name",
        "instrument_id", "holding_quantity", "cash_amount", "trade_history",
        "transaction_history", "api_key", "access_token",
    }
    for record in [*records.values(), market_map]:
        encoded = json.dumps(record).lower()
        assert not any(f'"{key}"' in encoded for key in prohibited_keys)
        assert "@" not in encoded


def test_legacy_sha_and_source_provenance(records, market_map):
    assert market_map["legacy_commit"] == LEGACY_SHA
    for record in records.values():
        assert record["legacy_commit"] == LEGACY_SHA
        assert record["legacy_repository"] == "Hybrid-Stock-Intelligence"
        assert record["legacy_sources"]
        assert all(source["path"] and source["symbol_or_heading"] for source in record["legacy_sources"])


def test_closure_covers_every_major_area():
    report = (DOCS / "LEGACY_HSI_EXTRACTION_CLOSURE.md").read_text(encoding="utf-8")
    areas = [
        "Evidence/governance", "Source hierarchy", "PIT/history",
        "61 diagnostics", "10-point score", "Six gates",
        "Strategy foundation", "Strategy taxonomy relationship", "Portfolio",
        "Rotation", "Sell-side", "Trim/profit taking", "Market context",
        "Liquidity/exitability",
    ]
    for area in areas:
        assert f"| {area} |" in report
    assert "YES_WITH_RECORDED_LIMITATIONS" in report
    assert "ARCHIVED_READ_ONLY_PROVENANCE_REFERENCE" in report
