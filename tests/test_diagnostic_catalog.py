"""Read-only contract checks for the V1 61-diagnostic knowledge extraction."""

from collections import Counter
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "hsi_knowledge" / "diagnostics"
CATALOG = BASE / "catalog"
SCHEMAS = ROOT / "hsi_knowledge" / "schema"
LEGACY_SHA = "f88b44d514fc9a2654040aa04e5350fc9e8660fe"
IDS = {f"D{number:02d}" for number in range(1, 62)}
V2_PENDING = {"D16", "D17", "D19", "D25", "D26", "D29"}
DETERMINISTIC_V1 = {f"D{number:02d}" for number in (
    1, 2, 4, 6, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 25, 26,
    29, 35, 36, 39, 43, 44, 45
)}
DUPLICATE_FAMILIES = {
    "base_pattern", "liquidity_pools", "ichimoku", "crowd_sentiment",
    "rvol", "sector_health", "quarterly_growth"
}


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def artifacts() -> dict[str, dict]:
    return {path.stem[:3]: read(path) for path in CATALOG.glob("*.json")}


@pytest.fixture(scope="module")
def index() -> dict:
    return read(BASE / "index.json")


@pytest.fixture(scope="module")
def evidence() -> dict:
    return read(BASE / "EVIDENCE_DEPENDENCY_CATALOG.json")


@pytest.fixture(scope="module")
def owners() -> dict:
    return read(BASE / "CALCULATION_OWNER_MAP.json")


@pytest.fixture(scope="module")
def validators():
    schemas = [read(path) for path in SCHEMAS.glob("*.schema.json")]
    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas
    )
    by_name = {schema["$id"].rsplit("/", 1)[-1]: schema for schema in schemas}
    return {
        name: Draft202012Validator(by_name[f"{name}.schema.json"],
                                   registry=registry, format_checker=FormatChecker())
        for name in ("knowledge", "diagnostic")
    }


def test_exactly_61_json_artifacts_and_ids(artifacts):
    paths = list(CATALOG.glob("*.json"))
    assert len(paths) == 61
    assert len(artifacts) == 61
    assert set(artifacts) == IDS
    assert {artifact["id"] for artifact in artifacts.values()} == IDS


def test_every_artifact_validates_against_both_schemas(artifacts, validators):
    for diagnostic_id, artifact in artifacts.items():
        for profile, instance in (("knowledge", artifact),
                                  ("diagnostic", artifact["details"])):
            errors = list(validators[profile].iter_errors(instance))
            assert not errors, (diagnostic_id, profile,
                                [error.message for error in errors])
        details = artifact["details"]
        assert details["diagnostic_id"] == artifact["id"]
        assert details["canonical_name"] == artifact["name"]
        assert details["version"] == artifact["version"]
        assert details["authority"] == artifact["authority_status"]
        assert details["lifecycle"] == artifact["status"]
        assert details["evidence_dependencies"] == artifact["evidence_dependencies"]


def test_no_diagnostic_active_or_runtime_calculation_owner(artifacts):
    assert all(artifact["status"] != "ACTIVE" for artifact in artifacts.values())
    assert all(artifact["effective_from"] is None for artifact in artifacts.values())
    assert all(artifact["deterministic_computation"] is False for artifact in artifacts.values())
    assert all(artifact["calculation_owner"] is None for artifact in artifacts.values())


@pytest.mark.parametrize("diagnostic_id,blocker", [
    ("D35", "NAMED_VWAP_SEMANTICS_UNAVAILABLE"),
    ("D57", "EVENT_EVIDENCE_NOT_READY"),
])
def test_unresolved_diagnostics_quarantined(artifacts, diagnostic_id, blocker):
    artifact = artifacts[diagnostic_id]
    assert artifact["authority_status"] == "CONFLICT_REVIEW_REQUIRED"
    assert artifact["status"] == "QUARANTINED"
    assert artifact["details"]["evaluation_type"] == "UNRESOLVED"
    assert any(conflict["code"] == blocker and
               conflict["resolution_status"] == "UNRESOLVED"
               for conflict in artifact["conflicts"])


def test_all_unknown_semantics_are_explicit_and_fail_closed(artifacts):
    for artifact in artifacts.values():
        semantics = artifact["details"]["result_semantics"]
        assert set(semantics) == {"PASS", "CAUTION", "FAIL", "UNKNOWN"}
        assert "never PASS" in semantics["UNKNOWN"]
        assert "Missing input is not CAUTION" in semantics["CAUTION"] or artifact["status"] == "QUARANTINED"


def test_deterministic_v1_rules_reference_normalized_evidence(artifacts, evidence):
    families = {entry["evidence_id"] for entry in evidence["evidence_families"]}
    for diagnostic_id in DETERMINISTIC_V1:
        dependencies = artifacts[diagnostic_id]["evidence_dependencies"]
        assert dependencies
        assert set(dependencies) <= families


def test_no_llm_calculation_owner(artifacts, evidence, owners):
    values = [entry["conceptual_owner"] for entry in evidence["evidence_families"]]
    values += [entry["conceptual_owner"] for entry in owners["calculation_families"]]
    values += [artifact["calculation_owner"] for artifact in artifacts.values()
               if artifact["calculation_owner"] is not None]
    assert not any("llm" in str(value).lower() for value in values)


def test_evidence_catalog_covers_every_dependency_and_consumers(artifacts, evidence):
    families = {entry["evidence_id"]: entry for entry in evidence["evidence_families"]}
    assert len(families) == len(evidence["evidence_families"])
    for diagnostic_id, artifact in artifacts.items():
        for dependency in artifact["evidence_dependencies"]:
            assert dependency in families
            assert diagnostic_id in families[dependency]["consumers"]
    for family in families.values():
        assert family["consumers"]
        assert all(family["evidence_id"] in artifacts[consumer]["evidence_dependencies"]
                   for consumer in family["consumers"])
        assert family["source_provenance"]["legacy_commit"] == LEGACY_SHA
        assert family["runtime_status"] == "NOT_IMPLEMENTED_IN_LITE"


def test_normalized_upstream_evidence_graph_is_resolved_and_acyclic(evidence):
    families = {entry["evidence_id"]: entry for entry in evidence["evidence_families"]}
    edges = {key: entry.get("upstream_evidence_dependencies", [])
             for key, entry in families.items()}
    assert all(set(upstream) <= set(families) and key not in upstream
               for key, upstream in edges.items())
    visited = set()
    active = set()

    def visit(key):
        assert key not in active, f"normalized evidence cycle at {key}"
        if key in visited:
            return
        active.add(key)
        for dependency in edges[key]:
            visit(dependency)
        active.remove(key)
        visited.add(key)

    for key in families:
        visit(key)
    assert edges["sector_rotation"] == ["sector_health"]
    assert "rvol" in edges["volume_climax"]
    assert "base_pattern" in edges["target_geometry"]


def test_calculation_owner_map_is_unique_and_not_implemented(owners, evidence):
    rows = owners["calculation_families"]
    keys = [row["calculation_id"] for row in rows]
    assert len(keys) == len(set(keys))
    deterministic = {entry["evidence_id"] for entry in evidence["evidence_families"]
                     if entry["deterministic"]}
    assert set(keys) == deterministic
    assert all(row["conceptual_owner"] and row["version"] == "0.1.0"
               and row["future_runtime_implementation_status"] == "NOT_IMPLEMENTED"
               for row in rows)


def test_seven_duplicate_families_have_exactly_one_owner(owners):
    counts = Counter(row["calculation_id"] for row in owners["calculation_families"])
    assert all(counts[family] == 1 for family in DUPLICATE_FAMILIES)


def test_all_22_duplicate_legacy_paths_are_transformed_once(artifacts, index, owners):
    duplicate_ids = {row["diagnostic_id"] for row in index["diagnostics"]
                     if row["legacy_audit_class"] == "DUPLICATE_COMPUTATION"}
    assert len(duplicate_ids) == 22
    removed_ids = [item["diagnostic_id"]
                   for owner in owners["calculation_families"]
                   for item in owner["duplicate_legacy_paths_removed_in_lite"]]
    assert len(removed_ids) == len(set(removed_ids)) == 22
    assert set(removed_ids) == duplicate_ids
    for diagnostic_id in duplicate_ids:
        artifact = artifacts[diagnostic_id]
        assert artifact["details"]["evaluation_type"] in {
            "PURE_CONSUMER", "COMPOSITE_RECONCILIATION"
        }
        assert any("Legacy DUPLICATE_COMPUTATION" in limitation
                   for limitation in artifact["known_limitations"])


def test_v2_successors_remain_inactive_and_v1_primary(artifacts):
    for diagnostic_id in V2_PENDING:
        artifact = artifacts[diagnostic_id]
        assert artifact["version"] == "1.0.0"
        assert artifact["status"] == "REVIEW_REQUIRED"
        assert "V1 meaning" in " ".join(artifact["known_limitations"])
        assert any("FUNDAMENTAL_DIAGNOSTIC_REGISTRY_V2_GOVERNANCE_APPROVAL"
                   in source["path"] for source in artifact["legacy_sources"])


def test_exact_legacy_provenance_and_no_broker_authority(artifacts):
    for artifact in artifacts.values():
        assert artifact["legacy_repository"] == "Hybrid-Stock-Intelligence"
        assert artifact["legacy_commit"] == LEGACY_SHA
        assert artifact["legacy_sources"]
        assert any(source["path"] == "app/registry/canonical.py" and
                   source["symbol_or_heading"] == "DIAGNOSTIC_RULES"
                   for source in artifact["legacy_sources"])
        assert "cannot override a gate" in artifact["details"]["gate_relationship"]
        assert "never creates setup, trade, BUY or SELL" in artifact["details"]["strategy_relationship"]


def test_index_exactly_references_catalog(artifacts, index):
    rows = index["diagnostics"]
    assert index["diagnostic_count"] == len(rows) == 61
    assert {row["diagnostic_id"] for row in rows} == IDS
    assert len({row["filename"] for row in rows}) == 61
    for row in rows:
        artifact = artifacts[row["diagnostic_id"]]
        assert read(BASE / row["filename"]) == artifact
        assert row["canonical_name"] == artifact["name"]
        assert row["authority_status"] == artifact["authority_status"]
        assert row["lifecycle"] == artifact["status"]
        assert row["evaluation_type"] == artifact["details"]["evaluation_type"]
        assert row["unresolved"] == (artifact["status"] == "QUARANTINED")
    assert Counter(row["legacy_audit_class"] for row in rows) == {
        "PURE_CONSUMER": 27, "JUSTIFIED_UNIQUE_CHECK": 10,
        "DUPLICATE_COMPUTATION": 22, "CONFLICTING_AUTHORITY": 1,
        "UNKNOWN_NEEDS_EXTRACTION": 1,
    }


def test_financial_inputs_keep_comparability_dependency(artifacts):
    for diagnostic_id in ("D16", "D17", "D18", "D19", "D20", "D24", "D25", "D26", "D27", "D28", "D29"):
        artifact = artifacts[diagnostic_id]
        assert "financial_comparability" in artifact["evidence_dependencies"]
        assert any("not zero/default" in limitation for limitation in artifact["known_limitations"])
