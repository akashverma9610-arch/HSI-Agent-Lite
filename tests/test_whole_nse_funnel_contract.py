"""Task #010 static whole-NSE funnel contracts; no scanning or providers."""

import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "hsi_knowledge" / "discovery"
EXPECTED_FILES = {
    "WHOLE_NSE_FUNNEL", "DISCOVERY_GATE_0_DATA_QUALITY",
    "DISCOVERY_GATE_1_INVESTABILITY", "DISCOVERY_GATE_2_RED_FLAGS",
    "DETECTOR_PRIMITIVE_CATALOG", "STRATEGY_DETECTOR_CATALOG",
    "CANDIDATE_UNION_CONTRACT", "PRELIMINARY_VALIDATION_CONTRACT",
    "DEEP_ANALYSIS_MODULE_MAP", "WHY_NOW_CONTRACT",
    "TECHNICAL_TIMING_CONTRACT", "REGIME_COMPATIBILITY_CONTRACT",
    "RISK_REWARD_STAGE_CONTRACT", "PORTFOLIO_FIT_CONTRACT",
    "DELIVERY_BUCKET_CONTRACT",
}
COSTS = {
    "C0_METADATA", "C1_CHEAP_DETERMINISTIC",
    "C2_MODERATE_DETERMINISTIC", "C3_DEEP_STRUCTURED_RESEARCH",
    "C4_AI_DEEP_RESEARCH",
}
BASELINE = "0c47679c81f311ed3a18fa8d53701fca1809aa22"


@pytest.fixture(scope="module")
def contracts():
    records = {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in DISCOVERY.glob("*.json")
    }
    assert set(records) == EXPECTED_FILES
    for name, record in records.items():
        assert record["contract_id"] == name
        assert record["status"] == "DESIGN_ONLY"
        assert record["lite_baseline_sha"] == BASELINE
        assert record["cost_class"] in COSTS
        assert record["runtime_implemented"] is False
        assert record["broker_order_authority"] is False
    return records


def test_funnel_stages_have_deterministic_order(contracts):
    funnel = contracts["WHOLE_NSE_FUNNEL"]
    stages = funnel["stages"]
    assert len(stages) == funnel["stage_count"] == 15
    assert [stage["order"] for stage in stages] == list(range(15))
    assert len({stage["stage_id"] for stage in stages}) == 15
    assert [stage["next_stage"] for stage in stages] == [
        stage["stage_id"] for stage in stages[1:]
    ] + [None]
    assert stages[0]["stage_id"] == "WHOLE_NSE_UNIVERSE"
    assert stages[-1]["stage_id"] == "FINAL_DELIVERY_BUCKET"


def test_discovery_gates_zero_to_two_exactly_once(contracts):
    stages = contracts["WHOLE_NSE_FUNNEL"]["stages"]
    actual = [stage["stage_id"] for stage in stages if stage["stage_id"].startswith("DISCOVERY_GATE_")]
    assert actual == [
        "DISCOVERY_GATE_0_DATA_QUALITY", "DISCOVERY_GATE_1_INVESTABILITY",
        "DISCOVERY_GATE_2_RED_FLAGS",
    ]
    assert [contracts[name]["gate_number"] for name in actual] == [0, 1, 2]


def test_discovery_gates_are_not_execution_gates(contracts):
    gate_ids = {
        item["gate_id"] for item in json.loads(
            (ROOT / "hsi_knowledge/gates/index.json").read_text(encoding="utf-8")
        )["gates"]
    }
    assert len(gate_ids) == 6
    for number in range(3):
        gate = contracts[contracts["WHOLE_NSE_FUNNEL"]["discovery_gate_ids"][number]]
        assert gate["execution_gate"] is False
        assert gate["contract_id"] not in gate_ids
    assert contracts["WHOLE_NSE_FUNNEL"]["discovery_gates_are_execution_gates"] is False


def test_bad_or_missing_data_non_evaluable_not_low_score(contracts):
    gate = contracts["DISCOVERY_GATE_0_DATA_QUALITY"]
    assert gate["missing_critical_evidence_outcome"] == "NON_EVALUABLE"
    assert gate["non_evaluable_is_low_investment_score"] is False
    assert gate["missing_evidence_is_zero"] is False
    assert "CONFLICTED_DATA" in gate["outcomes"]
    assert contracts["DELIVERY_BUCKET_CONTRACT"]["missing_data_defaults_to"] == "NON_EVALUABLE"


def test_market_cap_universe_configurable(contracts):
    cap = contracts["DISCOVERY_GATE_1_INVESTABILITY"]["market_cap_filter"]
    assert cap["configurable"] is True
    assert cap["default_numeric_bounds"] is None
    assert cap["preset_numeric_bounds_selected"] is False
    assert set(cap["presets"]) == {"MICRO", "SMALL_MID", "MID_LARGE", "ALL_NSE", "CUSTOM"}
    assert cap["founder_3000_30000_crore_range_is_mandatory"] is False
    assert contracts["WHOLE_NSE_FUNNEL"]["universe_size_fixed"] is False


def test_investability_contains_exitability(contracts):
    gate = contracts["DISCOVERY_GATE_1_INVESTABILITY"]
    dimensions = {item["dimension_id"]: item for item in gate["dimensions"]}
    assert "position_size_aware_exitability" in dimensions
    assert "days_to_exit_if_evidenced" in dimensions
    assert dimensions["position_size_aware_exitability"]["evaluation_phase"] == "DEFER_TO_PORTFOLIO_FIT_NOT_WHOLE_UNIVERSE"
    assert gate["no_universal_exit_days_threshold"] is True


def test_universal_vs_strategy_relative_red_flags(contracts):
    flags = contracts["DISCOVERY_GATE_2_RED_FLAGS"]
    assert flags["universal_red_flags"]
    assert flags["strategy_relative_examples"]
    assert flags["blanket_fundamental_metric_rejection_allowed"] is False
    assert any(item.get("may_be_thesis_context") == "DELEVERAGING"
               for item in flags["strategy_relative_examples"])
    assert all(item["cost_class"] in COSTS and item["evaluation_phase"]
               for item in flags["universal_red_flags"])
    assert next(item for item in flags["universal_red_flags"]
                if item["flag_id"] == "SEVERE_POSITION_EXITABILITY_ISSUE")["evaluation_phase"].startswith("DEFER_")


def test_all_35_archetypes_have_detectors(contracts):
    taxonomy_ids = {
        json.loads(path.read_text(encoding="utf-8"))["strategy_archetype_id"]
        for path in (ROOT / "hsi_knowledge/strategies/taxonomy").glob("*.json")
    }
    detectors = contracts["STRATEGY_DETECTOR_CATALOG"]["detectors"]
    assert len(taxonomy_ids) == len(detectors) == 35
    assert {item["archetype_id"] for item in detectors} == taxonomy_ids
    assert all((ROOT / item["taxonomy_ref"]).is_file() for item in detectors)


def test_detector_ids_and_archetypes_unique(contracts):
    detectors = contracts["STRATEGY_DETECTOR_CATALOG"]["detectors"]
    assert len({d["detector_id"] for d in detectors}) == len(detectors)
    assert len({d["archetype_id"] for d in detectors}) == len(detectors)
    assert all(d["detector_id"] == "DET_" + d["archetype_id"] for d in detectors)


def test_all_diagnostic_references_resolve(contracts):
    diagnostic_ids = {
        json.loads(path.read_text(encoding="utf-8"))["id"]
        for path in (ROOT / "hsi_knowledge/diagnostics/catalog").glob("*.json")
    }
    refs = set()
    refs.update(x for p in contracts["DETECTOR_PRIMITIVE_CATALOG"]["primitives"]
                for x in p["diagnostic_ids"])
    refs.update(x for d in contracts["STRATEGY_DETECTOR_CATALOG"]["detectors"]
                for x in d["cheap_diagnostic_ids"])
    refs.update(contracts["TECHNICAL_TIMING_CONTRACT"]["evidence_refs"])
    refs.update(contracts["RISK_REWARD_STAGE_CONTRACT"]["diagnostic_refs"])
    assert refs <= diagnostic_ids


def test_evidence_families_resolve_or_future_defined(contracts):
    catalog = json.loads(
        (ROOT / "hsi_knowledge/diagnostics/EVIDENCE_DEPENDENCY_CATALOG.json").read_text(encoding="utf-8")
    )
    existing = {item["evidence_id"] for item in catalog["evidence_families"]}
    primitives = contracts["DETECTOR_PRIMITIVE_CATALOG"]["primitives"]
    assert len({p["primitive_id"] for p in primitives}) == len(primitives)
    assert len({p["future_calculation_owner"] for p in primitives}) == len(primitives)
    for primitive in primitives:
        assert set(primitive["existing_evidence_families"]) <= existing
        assert primitive["existing_evidence_families"] or primitive["future_evidence_families"]
        assert primitive["future_calculation_owner"].startswith("future.discovery.")
        assert primitive["cost_class"] in COSTS - {"C3_DEEP_STRUCTURED_RESEARCH", "C4_AI_DEEP_RESEARCH"}


def test_cheap_detectors_never_require_default_c4_ai(contracts):
    primitive_map = {
        p["primitive_id"]: p for p in contracts["DETECTOR_PRIMITIVE_CATALOG"]["primitives"]
    }
    for detector in contracts["STRATEGY_DETECTOR_CATALOG"]["detectors"]:
        assert detector["ai_required"] is False
        assert detector["approved_investment"] is False
        assert detector["false_positive_tolerance"]
        assert detector["preliminary_trigger_semantics"]
        assert detector["escalation_destination"] == "PRELIMINARY_STRATEGY_VALIDATION"
        assert detector["future_runtime_cost_class"] in COSTS - {
            "C3_DEEP_STRUCTURED_RESEARCH", "C4_AI_DEEP_RESEARCH"
        }
        assert detector["cheap_evidence_dependencies"]
        for dependency in detector["cheap_evidence_dependencies"]:
            assert dependency["primitive_id"] in primitive_map
            assert dependency["cost_class"] == primitive_map[dependency["primitive_id"]]["cost_class"]
        expected_diagnostics = {
            diagnostic
            for dependency in detector["cheap_evidence_dependencies"]
            for diagnostic in primitive_map[dependency["primitive_id"]]["diagnostic_ids"]
        }
        assert set(detector["cheap_diagnostic_ids"]) == expected_diagnostics
    stages = contracts["WHOLE_NSE_FUNNEL"]["stages"]
    cheap = next(s for s in stages if s["stage_id"] == "CHEAP_STRATEGY_DETECTORS")
    assert "C4_AI_DEEP_RESEARCH" not in cheap["allowed_cost_classes"]


def test_same_security_can_trigger_multiple_detectors(contracts):
    union = contracts["CANDIDATE_UNION_CONTRACT"]
    assert union["one_security_may_trigger_multiple_detectors"] is True
    assert "triggered_archetype_ids" in union["output_fields"]
    assert "detector_result_refs" in union["output_fields"]


def test_candidate_union_preserves_triggers_without_evidence_duplication(contracts):
    union = contracts["CANDIDATE_UNION_CONTRACT"]
    assert "canonical_security_id" in union["merge_key"]
    assert "shared_evidence_ids" in union["output_fields"]
    assert "evidence_known_at" in union["output_fields"]
    assert "source_lineage_refs" in union["output_fields"]
    assert "detector_versions" in union["output_fields"]
    assert union["clone_underlying_evidence_per_strategy"] is False


def test_confluence_separate_from_detector_count(contracts):
    assert contracts["WHOLE_NSE_FUNNEL"]["detector_count_is_confluence"] is False
    assert contracts["CANDIDATE_UNION_CONTRACT"]["detector_count_is_confluence"] is False
    assert (ROOT / contracts["WHOLE_NSE_FUNNEL"]["confluence_source"]).is_file()


def test_why_now_not_universal_catalyst_gate(contracts):
    why = contracts["WHY_NOW_CONTRACT"]
    assert why["not_required_not_gate"] is True
    assert why["optional_not_gate"] is True
    assert why["quality_without_current_catalyst_can_remain_long_term_candidate"] is True
    assert why["event_presence_alone_validates_why_now"] is False
    assert any(d["catalyst_dependency_strength"] == "NOT_REQUIRED"
               for d in contracts["STRATEGY_DETECTOR_CATALOG"]["detectors"])


def test_technical_timing_separate_from_company_quality(contracts):
    timing = contracts["TECHNICAL_TIMING_CONTRACT"]
    assert timing["quality_and_timing_separate"] is True
    assert timing["strong_fundamentals_imply_good_entry"] is False
    assert "GOOD_COMPANY_BAD_TIMING" in timing["outcomes"]
    assert "NOT_APPLICABLE" in timing["outcomes"]


def test_regime_cannot_create_buy_or_sell(contracts):
    regime = contracts["REGIME_COMPATIBILITY_CONTRACT"]
    assert regime["can_create_buy"] is False
    assert regime["can_create_sell"] is False
    assert regime["unsupported_numeric_market_thresholds"] == []
    assert regime["stock_quality_equals_current_opportunity_quality"] is False
    taxonomy_ids = {
        json.loads(path.read_text(encoding="utf-8"))["strategy_archetype_id"]
        for path in (ROOT / "hsi_knowledge/strategies/taxonomy").glob("*.json")
    }
    profiles = regime["strategy_sensitivity_profiles"]
    assert len(profiles) == regime["profile_count"] == 35
    assert {p["archetype_id"] for p in profiles} == taxonomy_ids
    assert all(p["authority"] == "UNVALIDATED_SEMANTIC_DESIGN"
               and p["numeric_threshold"] is None
               and p["action_authority"] is False for p in profiles)


def test_risk_reward_has_no_universal_threshold(contracts):
    rr = contracts["RISK_REWARD_STAGE_CONTRACT"]
    assert rr["universal_minimum_risk_reward_threshold"] is None
    assert rr["high_quality_poor_asymmetry_can_be_watch"] is True
    assert rr["missing_reference_may_be_invented"] is False
    assert (ROOT / rr["geometry_authority_ref"]).is_file()


def test_portfolio_fit_cannot_mutate(contracts):
    fit = contracts["PORTFOLIO_FIT_CONTRACT"]
    assert fit["portfolio_mutation_allowed"] is False
    assert fit["individual_stock_strength_guarantees_fit"] is False
    assert fit["unknown_cash_is_zero"] is False
    assert all((ROOT / path).is_file() for path in fit["portfolio_knowledge_refs"])


def test_delivery_buckets_include_non_evaluable(contracts):
    delivery = contracts["DELIVERY_BUCKET_CONTRACT"]
    ids = [item["bucket_id"] for item in delivery["buckets"]]
    assert ids == [
        "A_ACTIONABLE_NOW", "B_ENTRY_WATCH", "C_RESEARCH_WATCH",
        "D_QUALITY_WRONG_PRICE", "E_REJECT_AVOID", "NON_EVALUABLE",
    ]
    assert delivery["bucket_count"] == len(ids) == 6


def test_actionable_now_has_no_broker_order_authority(contracts):
    delivery = contracts["DELIVERY_BUCKET_CONTRACT"]
    actionable = delivery["buckets"][0]
    assert actionable["requires_governed_execution_gate_pass"] is True
    assert actionable["broker_order_authority"] is False
    assert delivery["actionable_now_is_broker_order"] is False
    assert delivery["outputs_are_orders"] is False


def test_existing_execution_gate_fail_never_overridden(contracts):
    assert contracts["WHOLE_NSE_FUNNEL"]["execution_gate_fail_overridable"] is False
    assert contracts["RISK_REWARD_STAGE_CONTRACT"]["execution_gate_fail_overridable"] is False
    assert contracts["DELIVERY_BUCKET_CONTRACT"]["execution_gate_fail_overridable"] is False
    assert (ROOT / contracts["WHOLE_NSE_FUNNEL"]["execution_gate_catalog"]).is_file()


def test_no_runtime_network_provider_or_ai_code_added(contracts):
    assert {path.suffix for path in DISCOVERY.iterdir()} == {".json"}
    assert all(record["runtime_implemented"] is False for record in contracts.values())
    assert contracts["WHOLE_NSE_FUNNEL"]["compute_budget"]["c4_default_enabled"] is False
    assert contracts["DEEP_ANALYSIS_MODULE_MAP"]["c4_ai_deep_research"]["no_llm_called_in_this_task"] is True


def test_compute_budget_and_primitive_ownership(contracts):
    funnel = contracts["WHOLE_NSE_FUNNEL"]
    budget = funnel["compute_budget"]
    assert budget["deep_analysis_of_whole_universe_allowed"] is False
    assert budget["fixed_candidate_count"] is None
    stages = funnel["stages"]
    deep_order = next(s["order"] for s in stages if s["stage_id"] == "DEEP_HSI_ANALYSIS")
    prelim_order = next(s["order"] for s in stages if s["stage_id"] == "PRELIMINARY_STRATEGY_VALIDATION")
    assert prelim_order < deep_order
    assert all("C3_DEEP_STRUCTURED_RESEARCH" not in s["allowed_cost_classes"]
               and "C4_AI_DEEP_RESEARCH" not in s["allowed_cost_classes"]
               for s in stages[:deep_order])
    catalog = contracts["DETECTOR_PRIMITIVE_CATALOG"]
    assert catalog["primitive_count"] == len(catalog["primitives"])
    assert "never recalculate" in catalog["owner_rule"]


def test_all_lite_source_references_resolve(contracts):
    for name, record in contracts.items():
        for source in record.get("source_refs", []):
            assert (ROOT / source).exists(), (name, source)
    for stage in contracts["WHOLE_NSE_FUNNEL"]["stages"]:
        assert stage["default_cost_class"] in COSTS
        assert set(stage["allowed_cost_classes"]) <= COSTS
        assert stage["default_cost_class"] in stage["allowed_cost_classes"]
