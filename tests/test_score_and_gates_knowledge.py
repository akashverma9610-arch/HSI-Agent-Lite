"""Static Task #006 knowledge-contract checks; never compute a trading decision."""

import json
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "hsi_knowledge"
SCHEMAS = KNOWLEDGE / "schema"
SHA = "f88b44d514fc9a2654040aa04e5350fc9e8660fe"
POLICY = "six-gates-production-v1"
IDS = ["GATE_1_ROTATION", "GATE_2_VELOCITY", "GATE_3_SURVEILLANCE",
       "GATE_4_TRADE_PLAN", "GATE_5_HEAT", "GATE_6_EARNINGS"]
EXPECTED = {
    "earnings_acceleration": ("0.15", [24], [25, 26, 16, 27, 28]),
    "market_regime": ("0.10", [1], []),
    "sector_rotation": ("0.10", [2], [3]),
    "smart_money_evidence": ("0.10", [7], [9, 50, 58, 22]),
    "relative_strength": ("0.10", [6], []),
    "price_structure": ("0.10", [10], [4, 5, 37, 38, 40, 41, 42, 46]),
    "volume_obv_vwap": ("0.10", [11], [35, 36, 58]),
    "ichimoku_mtf": ("0.10", [12], [13, 14, 59]),
    "valuation_risk_reward": ("0.10", [29, 45], [43, 44, 31]),
    "liquidity_smc_traps": ("0.05", [8], [51, 52, 53, 54, 55, 56, 57, 60, 61]),
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validator(name):
    schema = read(SCHEMAS / f"{name}.schema.json")
    registry = Registry().with_resources(
        (item["$id"], Resource.from_contents(item))
        for path in SCHEMAS.glob("*.schema.json")
        if (item := read(path))
    )
    return Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())


def score():
    return read(KNOWLEDGE / "scoring/decision_score_v1.json")


def gates():
    return [read(path) for path in sorted((KNOWLEDGE / "gates/catalog").glob("*.json"))]


def diagnostic_ids():
    return {read(path)["id"] for path in (KNOWLEDGE / "diagnostics/catalog").glob("*.json")}


def evidence_ids():
    return {item["evidence_id"] for item in read(KNOWLEDGE / "diagnostics/EVIDENCE_DEPENDENCY_CATALOG.json")["evidence_families"]}


def test_exactly_one_score_and_six_v1_gates():
    assert [p.name for p in (KNOWLEDGE / "scoring").glob("decision_score*.json")] == ["decision_score_v1.json"]
    assert len(gates()) == 6
    assert [g["details"]["gate_id"] for g in gates()] == IDS
    index = read(KNOWLEDGE / "gates/index.json")
    assert index["gate_count"] == 6
    assert [item["gate_id"] for item in index["gates"]] == IDS
    assert all((KNOWLEDGE / "gates" / item["filename"]).is_file() for item in index["gates"])


def test_all_artifacts_validate_and_score_schema_is_narrow():
    item = score()
    assert validator("knowledge").is_valid(item)
    assert validator("score").is_valid(item["details"])
    for gate in gates():
        assert validator("knowledge").is_valid(gate)
        assert validator("gate").is_valid(gate["details"])
    invalid = read(KNOWLEDGE / "scoring/decision_score_v1.json")
    invalid["details"]["buy_sell_authority"] = True
    assert not validator("score").is_valid(invalid["details"])


def test_score_components_exact_weights_scale_and_missing_contract():
    details = score()["details"]
    assert (details["scale_min"], details["scale_max"]) == (0, 10)
    assert details["total_weight"] == "1.00"
    components = details["components"]
    assert len(components) == 10
    assert sum((Decimal(x["weight"]) for x in components), Decimal(0)) == Decimal("1.00")
    assert list(EXPECTED) == [x["component_id"] for x in components]
    for component in components:
        weight, mandatory, optional = EXPECTED[component["component_id"]]
        assert component["weight"] == weight
        assert component["mandatory_diagnostics"] == [f"D{n:02d}" for n in mandatory]
        assert component["optional_diagnostics"] == [f"D{n:02d}" for n in optional]
        assert component["mandatory_status"] == "ALL_REQUIRED"
    assert details["mandatory_missing_behavior"] == "COMPONENT_INELIGIBLE_SCORE_INCOMPLETE_FINAL_NULL"
    assert details["optional_missing_behavior"] == "COMPONENT_PARTIAL_NO_REWEIGHT"
    assert details["score_complete_rule"] == "ALL_COMPONENTS_NOT_INELIGIBLE"


def test_score_never_authorizes_trade_or_gate_override():
    d = score()["details"]
    assert d["buy_sell_authority"] is d["execution_authority"] is d["gate_override_allowed"] is d["broker_order_authority"] is False


def test_mandatory_unavailable_cannot_be_called_complete():
    details = score()["details"]
    required = {d for c in details["components"] for d in c["mandatory_diagnostics"]}
    admitted = required - {"D01"}
    ineligible = [c for c in details["components"]
                  if not set(c["mandatory_diagnostics"]) <= admitted]
    assert [c["component_id"] for c in ineligible] == ["market_regime"]
    assert details["score_complete_rule"] == "ALL_COMPONENTS_NOT_INELIGIBLE"
    assert details["mandatory_missing_behavior"] == "COMPONENT_INELIGIBLE_SCORE_INCOMPLETE_FINAL_NULL"


def test_gate_outcomes_fail_closed_no_score_or_llm_override():
    for item in gates():
        d = item["details"]
        assert d["pass_condition"]["description"] and d["fail_condition"]["description"]
        assert d["unknown_behavior"] == "BLOCK"
        assert d["score_or_llm_override_allowed"] is False
        assert d["broker_order_authority"] is False
        assert d["criticality"] == "CRITICAL"
        assert "override" in d["score_interaction"].lower() or "rescue" in d["score_interaction"].lower()
    assert "missing plan is **FAIL**" in (ROOT / "docs/SIX_EXECUTION_GATES_EXTRACTION.md").read_text(encoding="utf-8")


def test_dependency_maps_resolve_and_are_not_runtime():
    known_d, known_e = diagnostic_ids(), evidence_ids()
    smap = read(KNOWLEDGE / "scoring/SCORE_DEPENDENCY_MAP.json")
    gmap = read(KNOWLEDGE / "gates/GATE_DEPENDENCY_MAP.json")
    assert len(smap["components"]) == 10 and len(gmap["gates"]) == 6
    assert [item["gate_id"] for item in gmap["gates"]] == IDS
    for item in smap["components"]:
        assert set(item["mandatory_diagnostics"] + item["optional_diagnostics"]) <= known_d
        assert set(item["indirect_evidence_families"]) <= known_e
        expected_evidence = set().union(*(
            set(read(next((KNOWLEDGE / "diagnostics/catalog").glob(f"{d}_*.json")))["evidence_dependencies"])
            for d in item["mandatory_diagnostics"] + item["optional_diagnostics"]
        ))
        assert set(item["indirect_evidence_families"]) == expected_evidence
        assert item["future_calculation_owner"].endswith("NOT_IMPLEMENTED")
    for item in gmap["gates"]:
        assert set(item["diagnostic_dependencies"]) <= known_d
        assert set(item["evidence_family_dependencies"]) <= known_e
        assert item["future_runtime_status"] == "NOT_IMPLEMENTED_IN_LITE"


def test_quarantine_impact_and_v2_never_active():
    smap = read(KNOWLEDGE / "scoring/SCORE_DEPENDENCY_MAP.json")
    impact = {entry["diagnostic_id"]: entry["effect"]
              for component in smap["components"] for entry in component["quarantine_impact"]}
    assert set(impact) == {"D35", "D57"}
    assert all("OPTIONAL_UNAVAILABLE" in value and "NO_SUBSTITUTE" in value for value in impact.values())
    assert score()["details"]["quarantined_dependencies"] == ["D35", "D57"]
    assert all(read(next((KNOWLEDGE / "diagnostics/catalog").glob(f"{d}_*.json")))["status"] == "QUARANTINED" for d in impact)
    v2 = read(KNOWLEDGE / "gates/V2_SUCCESSOR_MAP.json")
    assert v2["activation_status"] == v2["lite_activation_status"] == "NOT_ACTIVE"
    assert v2["no_runtime_activation"] is True and v2["global_blockers"]
    assert v2["successor_policy_id"] != POLICY
    assert all(POLICY not in gate["id"] or gate["details"]["lifecycle"] == "REVIEW_REQUIRED" for gate in gates())


def test_provenance_lifecycle_and_no_runtime_code():
    for item in [score(), *gates()]:
        assert item["legacy_commit"] == SHA
        assert item["legacy_repository"] == "Hybrid-Stock-Intelligence"
        assert item["legacy_sources"] and item["status"] == "REVIEW_REQUIRED"
        assert item["deterministic_computation"] is False and item["calculation_owner"] is None
    assert all(g["details"]["lifecycle"] == "REVIEW_REQUIRED" for g in gates())
    assert not (KNOWLEDGE / "scoring/engine.py").exists()
    assert not (KNOWLEDGE / "gates/engine.py").exists()
    assert not any((KNOWLEDGE / "scoring").glob("*.py"))
    assert not any((KNOWLEDGE / "gates").glob("*.py"))
