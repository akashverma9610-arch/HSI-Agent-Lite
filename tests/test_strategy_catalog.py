"""Static Task #007 strategy knowledge contracts; no strategy evaluator."""

import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "hsi_knowledge"
STRATEGIES = K / "strategies"
SCHEMAS = K / "schema"
SHA = "f88b44d514fc9a2654040aa04e5350fc9e8660fe"
IDS = ["PRE_BREAKOUT", "TACTICAL", "POSITIONAL", "LONG_TERM", "EVENT_CATALYST", "MARKET_RED_RESILIENCE"]
AUTHORITY = {
    "PRE_BREAKOUT": "LATEST_ACCEPTED_WITH_LIMITATIONS",
    "TACTICAL": "PROPOSED_NOT_ACTIVE",
    "POSITIONAL": "LATEST_ACCEPTED_WITH_LIMITATIONS",
    "LONG_TERM": "PROPOSED_NOT_ACTIVE",
    "EVENT_CATALYST": "PROPOSED_NOT_ACTIVE",
    "MARKET_RED_RESILIENCE": "PROPOSED_NOT_ACTIVE",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validator(name):
    schema = read(SCHEMAS / f"{name}.schema.json")
    registry = Registry().with_resources(
        (other["$id"], Resource.from_contents(other))
        for path in SCHEMAS.glob("*.schema.json") if (other := read(path))
    )
    return Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())


def catalog():
    return {item["details"]["strategy_id"]: item for path in sorted((STRATEGIES / "catalog").glob("*.json"))
            if (item := read(path))}


def registry():
    return read(STRATEGIES / "registry.json")


def test_six_artifacts_unique_versions_and_registry_exact_files():
    files = sorted((STRATEGIES / "catalog").glob("*.json"))
    assert len(files) == 6
    assert set(catalog()) == set(IDS)
    assert len(set(item["id"] for item in catalog().values())) == 6
    entries = registry()["entries"]
    assert [item["strategy_id"] for item in entries] == IDS
    assert len({(item["strategy_id"], item["strategy_version"]) for item in entries}) == 6
    assert {item["filename"] for item in entries} == {f"catalog/{p.name}" for p in files}
    assert all(re.fullmatch(r"\d+\.\d+\.\d+", item["strategy_version"]) for item in entries)
    for entry in entries:
        item = read(STRATEGIES / entry["filename"])
        assert item["id"] == entry["strategy_id"] == entry["strategy_family"]
        assert item["version"] == item["details"]["version"] == entry["strategy_version"]
        assert item["authority_status"] == entry["authority_status"]
        assert item["status"] == entry["lite_lifecycle"]


def test_registry_entries_have_modular_contract_fields():
    required = {
        "strategy_id", "strategy_family", "strategy_version", "filename", "authority_status",
        "lite_lifecycle", "legacy_lifecycle_status", "purpose", "horizon_status",
        "required_diagnostics", "optional_diagnostics", "context_diagnostics",
        "quarantined_diagnostics", "required_evidence_families", "required_gates",
        "gate_applicability", "entry_policy_status", "invalidation_policy_status",
        "target_policy_status", "portfolio_use_status", "blockers", "future_runtime_status",
    }
    for entry in registry()["entries"]:
        assert required <= set(entry)
        assert entry["blockers"]
        assert set(entry["required_gates"]) == {g["gate_id"] for g in entry["gate_applicability"]}
        assert entry["horizon_status"] == "INTENDED_HORIZON_ONLY"


def test_every_artifact_validates_both_profiles_and_provenance():
    for item in catalog().values():
        assert validator("knowledge").is_valid(item)
        assert validator("strategy").is_valid(item["details"])
        assert item["legacy_commit"] == SHA
        assert item["legacy_repository"] == "Hybrid-Stock-Intelligence"
        assert item["legacy_sources"] and item["details"]["provenance"]
        assert item["deterministic_computation"] is False and item["calculation_owner"] is None
        assert item["details"]["validation_evidence"]
    assert registry()["legacy_commit"] == SHA


def test_authority_and_lifecycle_fail_closed():
    entries = {entry["strategy_id"]: entry for entry in registry()["entries"]}
    for strategy_id, authority in AUTHORITY.items():
        assert entries[strategy_id]["authority_status"] == authority
        assert entries[strategy_id]["lite_lifecycle"] in {"REVIEW_REQUIRED", "EXTRACTED_DRAFT"}
        assert entries[strategy_id]["future_runtime_status"] == "NOT_IMPLEMENTED_IN_LITE"
        if authority == "PROPOSED_NOT_ACTIVE":
            assert entries[strategy_id]["lite_lifecycle"] != "ACTIVE"
    r = registry()
    assert r["unknown_strategy_result"] == "STRATEGY_UNAVAILABLE"
    assert r["proposed_strategy_active_use_result"] == "STRATEGY_UNAVAILABLE"
    assert r["unapproved_version_result"] == "STRATEGY_UNAVAILABLE"
    assert r["registry_presence_is_approval"] is False
    assert r["approval_is_runtime_activation"] is False


def test_prebreakout_watch_only_and_no_geometry_leakage():
    c = catalog()
    pre = c["PRE_BREAKOUT"]["details"]
    tactical = c["TACTICAL"]["details"]
    positional = c["POSITIONAL"]["details"]
    assert "WATCH_ONLY_NON_EXECUTABLE" in pre["legacy_lifecycle"]
    assert pre["lifecycle"] == "REVIEW_REQUIRED"
    assert pre["geometry_authority"] == "PRE_BREAKOUT_GOVERNED_POLICY_SELECTION"
    assert all(pre[x] for x in ("entry_policy_reference", "invalidation_policy_reference", "target_policy_reference"))
    assert pre["portfolio_permissions"]["may_inform_watch"] is True
    assert len(pre["prebreakout_evidence_contract"]["technical_checks"]) == 6
    assert "known-at" in pre["prebreakout_evidence_contract"]["source_readiness"]
    assert pre["score_relationship"]["role"] == "NOT_AUTHORITATIVE"
    assert "known-at" in " ".join(pre["known_blockers"]).lower()
    assert tactical["geometry_authority"] == "UNAVAILABLE"
    assert all(tactical[x] is None for x in ("entry_policy_reference", "invalidation_policy_reference", "target_policy_reference"))
    assert positional["strategy_id"] != pre["strategy_id"]
    assert positional["geometry_authority"].startswith("UNAVAILABLE_GENERIC")
    assert all(positional[x] is None for x in ("entry_policy_reference", "invalidation_policy_reference", "target_policy_reference"))


def test_research_families_do_not_fabricate_policies_or_sponsorship():
    c = catalog()
    long_term = c["LONG_TERM"]["details"]
    event = c["EVENT_CATALYST"]["details"]
    red = c["MARKET_RED_RESILIENCE"]["details"]
    assert len(long_term["research_subfamilies"]) == 5
    for d in (long_term, event, red):
        assert all(d[x] is None for x in ("entry_policy_reference", "invalidation_policy_reference", "target_policy_reference"))
        assert d["geometry_authority"] == "UNAVAILABLE"
        assert d["deterministic_eligibility"] == []
    assert "materiality" in " ".join(event["unavailable_dependencies"]).lower()
    assert "expiry" in " ".join(event["unavailable_dependencies"]).lower()
    assert not any("threshold=" in text or "window=" in text for text in event["interpretive_guidance"])
    assert "does NOT prove institutional sponsorship" in " ".join(red["interpretive_guidance"])


def test_quarantined_diagnostics_remain_unusable():
    c = catalog()
    for diagnostic_id, strategy_id in (("D57", "EVENT_CATALYST"), ("D35", "TACTICAL")):
        d = c[strategy_id]["details"]
        assert diagnostic_id in d["quarantined_diagnostics"]
        assert diagnostic_id not in d["required_diagnostics"] + d["optional_diagnostics"]
        artifact = read(next((K / "diagnostics/catalog").glob(f"{diagnostic_id}_*.json")))
        assert artifact["status"] == "QUARANTINED"
    assert "cannot become valid" in " ".join(c["EVENT_CATALYST"]["details"]["interpretive_guidance"])


def test_all_diagnostics_evidence_and_gate_references_resolve():
    diagnostics = {read(p)["id"] for p in (K / "diagnostics/catalog").glob("*.json")}
    evidence = {item["evidence_id"] for item in read(K / "diagnostics/EVIDENCE_DEPENDENCY_CATALOG.json")["evidence_families"]}
    gates = {item["gate_id"] for item in read(K / "gates/index.json")["gates"]}
    assert len(gates) == 6
    for strategy_id, artifact in catalog().items():
        d = artifact["details"]
        assert set(d["required_diagnostics"] + d["optional_diagnostics"] + d["context_diagnostics"] + d["quarantined_diagnostics"]) <= diagnostics
        assert set(d["required_evidence"]) <= evidence
        assert set(d["gate_dependencies"]) == gates
        assert {x["gate_id"] for x in d["gate_applicability"]} == gates
        if strategy_id != "PRE_BREAKOUT":
            assert all(x["status"] == "UNRESOLVED" for x in d["gate_applicability"])
        assert d["gate_fail_override_allowed"] is False
        assert d["score_substitutes_for_eligibility"] is False
        assert d["score_relationship"]["minimum_score"] is None
        assert d["broker_order_authority"] is False
        assert d["recalculates_evidence_metrics"] is False
        assert d["portfolio_permissions"]["may_authorize_rotation"] is False
        assert d["portfolio_permissions"]["may_authorize_trim"] is False
        assert d["portfolio_permissions"]["may_authorize_broker_order"] is False


def test_geometry_and_horizon_maps_are_non_universal_and_unvalidated():
    geometry = read(STRATEGIES / "GEOMETRY_AUTHORITY_MAP.json")
    horizon = read(STRATEGIES / "HORIZON_AUTHORITY_MAP.json")
    assert geometry["universal_geometry_authority"] is None
    assert geometry["legacy_commit"] == horizon["legacy_commit"] == SHA
    assert geometry["generic_diagnostic_geometry"]["authority"] == "CONFLICT_REVIEW_REQUIRED"
    assert set(geometry["generic_diagnostic_geometry"]["diagnostic_ids"]) <= {
        read(p)["id"] for p in (K / "diagnostics/catalog").glob("*.json")
    }
    assert {x["strategy_id"] for x in geometry["strategies"]} == set(IDS)
    assert all(x["trading_geometry_approved_for_lite"] is False for x in geometry["strategies"])
    assert {x["strategy_id"] for x in horizon["strategies"]} == set(IDS)
    assert "INTENDED_HORIZON" in horizon["distinction"] and "VALIDATED_HORIZON" in horizon["distinction"]
    assert all(x["intended_horizon_status"] == "INTENDED_HORIZON" and x["validated_horizon"] is None
               and x["calibrated"] is False and x["production_approved"] is False for x in horizon["strategies"])
    assert all(item["details"]["horizon_status"] == "INTENDED_HORIZON_ONLY" for item in catalog().values())


def test_no_strategy_runtime_added():
    assert not any(STRATEGIES.rglob("*.py"))
    assert not (ROOT / "app/strategies").exists()
