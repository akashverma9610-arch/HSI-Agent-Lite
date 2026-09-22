"""Schema-contract tests using only synthetic local fixtures."""

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "hsi_knowledge" / "schema"
FIXTURES = ROOT / "tests" / "fixtures" / "knowledge"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validator(name: str) -> Draft202012Validator:
    schema = load(SCHEMAS / f"{name}.schema.json")
    Draft202012Validator.check_schema(schema)
    registry = Registry().with_resources(
        (other["$id"], Resource.from_contents(other))
        for path in SCHEMAS.glob("*.schema.json")
        if (other := load(path))
    )
    return Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())


def fixture(name: str) -> dict:
    return load(FIXTURES / f"{name}.json")


def assert_valid(profile: str, instance: dict) -> None:
    errors = list(validator(profile).iter_errors(instance))
    assert not errors, [error.message for error in errors]


def assert_invalid(profile: str, instance: dict) -> None:
    assert list(validator(profile).iter_errors(instance))


def test_all_schemas_parse_and_validate_as_schemas():
    assert {p.name for p in SCHEMAS.glob("*.schema.json")} == {
        "knowledge.schema.json", "evidence.schema.json", "diagnostic.schema.json",
        "strategy.schema.json", "gate.schema.json",
    }
    for name in ("knowledge", "evidence", "diagnostic", "strategy", "gate"):
        validator(name)


def test_valid_synthetic_fixtures():
    artifact = fixture("artifact")
    assert_valid("knowledge", artifact)
    assert_valid("diagnostic", artifact["details"])
    assert_valid("evidence", fixture("evidence"))
    assert_valid("gate", fixture("gate"))
    assert_valid("strategy", fixture("strategy"))


def test_missing_provenance_fails():
    artifact = fixture("artifact")
    del artifact["legacy_sources"]
    assert_invalid("knowledge", artifact)


def test_unknown_authority_status_fails():
    artifact = fixture("artifact")
    artifact["authority_status"] = "AUTO_APPROVED"
    assert_invalid("knowledge", artifact)


def test_profile_is_enforced_by_envelope():
    artifact = fixture("artifact")
    del artifact["details"]["result_semantics"]["UNKNOWN"]
    assert_invalid("knowledge", artifact)


@pytest.mark.parametrize("authority", [
    "PROPOSED_NOT_ACTIVE", "HISTORICAL_ONLY", "CONFLICT_REVIEW_REQUIRED", "NOT_FOUND"
])
def test_invalid_lifecycle_escalation_fails(authority):
    artifact = fixture("artifact")
    artifact.update(status="ACTIVE", authority_status=authority,
                    extraction_status="VERIFIED", review_status="HUMAN_APPROVED",
                    effective_from="2026-01-01T00:00:00Z")
    assert_invalid("knowledge", artifact)


def test_active_requires_review_effective_time_and_closed_conflicts():
    artifact = fixture("artifact")
    artifact["status"] = "ACTIVE"
    assert_invalid("knowledge", artifact)
    artifact.update(extraction_status="VERIFIED", review_status="HUMAN_APPROVED",
                    effective_from="2026-01-01T00:00:00Z")
    artifact["details"]["lifecycle"] = "ACTIVE"
    artifact["conflicts"] = [{"code": "synthetic", "description": "Unresolved",
                               "resolution_status": "UNRESOLVED"}]
    assert_invalid("knowledge", artifact)
    artifact["conflicts"][0]["resolution_status"] = "RESOLVED_WITH_REVIEW"
    assert_valid("knowledge", artifact)


def test_active_needs_accepted_approval_or_contract_source():
    artifact = fixture("artifact")
    artifact.update(status="ACTIVE", extraction_status="VERIFIED",
                    review_status="HUMAN_APPROVED",
                    effective_from="2026-01-01T00:00:00Z")
    artifact["details"]["lifecycle"] = "ACTIVE"
    artifact["legacy_sources"][0]["source_role"] = "PROPOSAL"
    assert_invalid("knowledge", artifact)


def test_deterministic_computation_requires_owner():
    artifact = fixture("artifact")
    artifact["deterministic_computation"] = True
    assert_invalid("knowledge", artifact)
    artifact["calculation_owner"] = {"computation_id": "synthetic.owner",
                                     "computation_version": "0.1.0"}
    assert_valid("knowledge", artifact)


def test_unprofiled_artifact_type_cannot_activate():
    artifact = fixture("artifact")
    artifact.update(artifact_type="governance_policy", status="ACTIVE",
                    extraction_status="VERIFIED", review_status="HUMAN_APPROVED",
                    effective_from="2026-01-01T00:00:00Z")
    assert_invalid("knowledge", artifact)


def test_evidence_without_source_timestamp_fails():
    evidence = fixture("evidence")
    evidence["source_timestamps"] = []
    assert_invalid("evidence", evidence)
    del evidence["source_timestamps"]
    assert_invalid("evidence", evidence)


def test_diagnostic_requires_unknown_semantics():
    diagnostic = fixture("artifact")["details"]
    del diagnostic["result_semantics"]["UNKNOWN"]
    assert_invalid("diagnostic", diagnostic)


def test_gate_requires_fail_closed_unknown_behavior_and_no_override():
    gate = fixture("gate")
    del gate["unknown_behavior"]
    assert_invalid("gate", gate)
    gate = fixture("gate")
    gate["score_or_llm_override_allowed"] = True
    assert_invalid("gate", gate)


@pytest.mark.parametrize("profile,fixture_name", [
    ("knowledge", "artifact"), ("evidence", "evidence"),
    ("diagnostic", "artifact"), ("strategy", "strategy"), ("gate", "gate")
])
def test_arbitrary_extra_fields_rejected(profile, fixture_name):
    instance = fixture(fixture_name)
    if profile == "diagnostic":
        instance = copy.deepcopy(instance["details"])
    instance["unreviewed_extra"] = "not allowed"
    assert_invalid(profile, instance)


def test_quarantined_duplicate_cannot_activate():
    diagnostic = fixture("artifact")["details"]
    diagnostic["evaluation_type"] = "QUARANTINED_DUPLICATE"
    diagnostic["lifecycle"] = "ACTIVE"
    assert_invalid("diagnostic", diagnostic)
