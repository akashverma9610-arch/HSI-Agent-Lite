"""Local, non-runtime checks for the Task #004 governance extraction."""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = ROOT / "hsi_knowledge" / "governance"
SCHEMA_DIR = ROOT / "hsi_knowledge" / "schema"
LEGACY_SHA = "f88b44d514fc9a2654040aa04e5350fc9e8660fe"
EXPECTED = {
    "evidence_discipline": "AUTHORITATIVE_ACCEPTED",
    "source_hierarchy": "AUTHORITATIVE_ACCEPTED",
    "data_reliability": "LATEST_ACCEPTED_WITH_LIMITATIONS",
    "historical_pit": "LATEST_ACCEPTED_WITH_LIMITATIONS",
    "model_governance": "AUTHORITATIVE_ACCEPTED",
    "prospective_validation": "LATEST_ACCEPTED_WITH_LIMITATIONS",
    "signal_watch": "LATEST_ACCEPTED_WITH_LIMITATIONS",
    "strategy_registry": "LATEST_ACCEPTED_WITH_LIMITATIONS",
    "macro_news": "LATEST_ACCEPTED_WITH_LIMITATIONS",
}


def artifacts() -> dict[str, dict]:
    return {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in KNOWLEDGE_DIR.glob("*.json")
    }


def schema_validator() -> Draft202012Validator:
    schemas = [json.loads(path.read_text(encoding="utf-8"))
               for path in SCHEMA_DIR.glob("*.schema.json")]
    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas
    )
    knowledge = next(schema for schema in schemas
                     if schema["$id"].endswith("/knowledge.schema.json"))
    return Draft202012Validator(knowledge, registry=registry,
                               format_checker=FormatChecker())


@pytest.fixture(scope="module")
def records() -> dict[str, dict]:
    return artifacts()


def test_all_artifacts_validate_against_task_003_schema(records):
    validator = schema_validator()
    for filename, artifact in records.items():
        errors = list(validator.iter_errors(artifact))
        assert not errors, (filename, [error.message for error in errors])


def test_expected_domains_exactly_once_and_authority_preserved(records):
    assert set(records) == {"macro_news_governance", *(EXPECTED.keys() - {"macro_news"})}
    assert len({record["id"] for record in records.values()}) == len(EXPECTED)
    assert {record["id"]: record["authority_status"] for record in records.values()} == EXPECTED


def test_legacy_provenance_exists(records):
    for record in records.values():
        assert record["legacy_repository"] == "Hybrid-Stock-Intelligence"
        assert record["legacy_sources"]
        for source in record["legacy_sources"]:
            assert source["path"] and source["symbol_or_heading"]
            assert source["authority"] and source["source_role"]


def test_no_proposed_artifact_is_active(records):
    assert all(record["status"] != "ACTIVE"
               for record in records.values()
               if record["authority_status"] == "PROPOSED_NOT_ACTIVE")


def test_unresolved_conflict_is_not_active(records):
    assert all(record["status"] != "ACTIVE"
               for record in records.values()
               if any(conflict["resolution_status"] == "UNRESOLVED"
                      for conflict in record["conflicts"]))


def test_missing_evidence_cannot_mean_pass(records):
    details = records["evidence_discipline"]["details"]
    assert details["evidence_chain"] == ["FACT", "DATA", "INTERPRETATION", "INFERENCE"]
    assert details["missing_evidence_outcome"] == "UNKNOWN_OR_UNAVAILABLE"
    assert details["missing_evidence_can_mean_pass"] is False
    assert details["missing_evidence_can_mean_zero"] is False
    assert details["missing_evidence_can_mean_neutral"] is False
    assert details["unsupported_confidence_allowed"] is False


def test_model_governance_requires_human_review_before_activation(records):
    details = records["model_governance"]["details"]
    sequence = details["promotion_sequence"]
    assert sequence.index("HUMAN_REVIEW") < sequence.index("APPROVED_VERSION")
    assert sequence.index("APPROVED_VERSION") < sequence.index("SEPARATE_ACTIVATION")
    assert details["human_review_required_before_activation"] is True
    assert details["drift_observation_can_auto_deploy"] is False


def test_watch_is_non_executable(records):
    details = records["signal_watch"]["details"]
    assert details["actionability"] == "WATCH_ONLY"
    assert details["execution_status"] == "NON_EXECUTABLE"
    assert details["consumer_active"] is False
    assert details["signal_existence_implies_order_authority"] is False


def test_registry_presence_does_not_mean_active(records):
    details = records["strategy_registry"]["details"]
    assert details["registered_implies_approved"] is False
    assert details["registered_implies_active"] is False
    assert details["unavailable_resolution"] == "STRATEGY_UNAVAILABLE"


def test_macro_news_cannot_directly_authorize_trade(records):
    details = records["macro_news_governance"]["details"]
    assert details["role"] == "CONTEXTUAL_EVIDENCE"
    assert details["news_directly_authorizes_trade"] is False
    assert details["event_catalyst_strategy_parameters_included"] is False
    assert details["same_event_counts_as_multiple_confirmations"] is False


def test_legacy_commit_matches_extraction_baseline(records):
    assert all(record["legacy_commit"] == LEGACY_SHA for record in records.values())


def test_no_artifact_contains_broker_order_authority(records):
    for record in records.values():
        assert record["details"]["direct_trade_authority"] is False
        assert record["artifact_type"] == "governance_policy"
        assert record["deterministic_computation"] is False
        assert record["calculation_owner"] is None


def test_schema_boundary_is_not_silently_bypassed(records):
    assert all(record["status"] == "REVIEW_REQUIRED" for record in records.values())
    assert all(record["extraction_status"] == "VERIFIED" for record in records.values())
    assert all(record["review_status"] == "IN_REVIEW" for record in records.values())
    assert all(record["effective_from"] is None for record in records.values())
