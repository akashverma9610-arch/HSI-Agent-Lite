"""Task #008 static taxonomy/confluence contracts; no eligibility or scoring runtime."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "hsi_knowledge"
S = K / "strategies"
T = S / "taxonomy"
SHA = "f88b44d514fc9a2654040aa04e5350fc9e8660fe"
FAMILIES = {
    "FAMILY_A_BUSINESS_EARNINGS", "FAMILY_B_PRICE_FLOW", "FAMILY_C_RECOVERY_RERATING",
    "FAMILY_D_INDUSTRY_CYCLE", "FAMILY_E_CATALYST", "FAMILY_F_STRUCTURAL_GROWTH",
}
DIMENSIONS = {
    "FUNDAMENTALS", "EARNINGS", "TECHNICALS", "VALUATION", "CATALYST_NEWS",
    "SECTOR_MACRO", "FLOW", "BALANCE_SHEET_CASH_FLOW", "MANAGEMENT_GOVERNANCE",
    "LIQUIDITY_EXITABILITY",
}
EXPECTED_IDS = {
    "FUNDAMENTAL_INFLECTION", "MID_TERM_COMPOUNDER", "LONG_TERM_STRUCTURAL_COMPOUNDER",
    "PRE_BREAKOUT_ACCUMULATION", "CONFIRMED_BREAKOUT", "BREAKOUT_RETEST",
    "EARNINGS_MOMENTUM", "EARNINGS_SURPRISE_POST_RESULT_DRIFT", "MARGIN_EXPANSION",
    "CASH_FLOW_INFLECTION", "DELEVERAGING", "TURNAROUND_RECOVERY", "RERATING_CANDIDATE",
    "QARP", "GARP", "DEEP_VALUE_MEAN_REVERSION", "CYCLICAL_RECOVERY",
    "COMMODITY_UPCYCLE", "SECTOR_ROTATION_LEADER", "MARKET_RED_RESILIENCE",
    "INSTITUTIONAL_ACCUMULATION", "ORDER_BOOK_CAPEX_CYCLE", "CAPACITY_EXPANSION",
    "EVENT_CATALYST", "SPECIAL_SITUATION", "DEMERGER_VALUE_UNLOCK",
    "IMPORT_SUBSTITUTION", "EXPORT_SCALING", "MARKET_SHARE_GAINER",
    "NEW_PRODUCT_NEW_CUSTOMER_INFLECTION", "PROMOTER_MANAGEMENT_TRANSFORMATION",
    "ASSET_MONETISATION", "POLICY_REGULATORY_BENEFICIARY",
    "DOMESTIC_CAPEX_BENEFICIARY", "EARLY_EMERGING_LEADER_SMALL_MIDCAP",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def taxonomy():
    return {item["strategy_archetype_id"]: item for path in T.glob("*.json") if (item := read(path))}


def test_exact_35_unique_schema_valid_archetypes_and_six_families():
    files = list(T.glob("*.json"))
    assert len(files) == 35
    items = taxonomy()
    assert len(items) == 35 and set(items) == EXPECTED_IDS
    schema = read(K / "schema/strategy_archetype.schema.json")
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    assert {a["primary_family"] for a in items.values()} == FAMILIES
    aliases = [alias for item in items.values() for alias in item["aliases"]]
    assert len(aliases) == len(set(aliases))
    assert not (set(aliases) & set(items))
    for item in items.values():
        assert not list(validator.iter_errors(item))
        assert item["primary_family"] not in item["secondary_families"]
        assert set(item["secondary_families"]) <= FAMILIES
        assert set(item["dependency_strengths"]) == DIMENSIONS
        assert set(item["dependency_strengths"].values()) <= {"PRIMARY", "SECONDARY", "OPTIONAL", "NOT_REQUIRED"}
        assert item["primary_dependencies"]
        assert any(x == "NOT_REQUIRED" for x in item["dependency_strengths"].values())
        assert item["version"] == "0.1.0"


def test_schema_rejects_founder_design_activation_without_new_authority():
    schema = read(K / "schema/strategy_archetype.schema.json")
    validator = Draft202012Validator(schema)
    item = dict(taxonomy()["QARP"])
    item.update(lifecycle="ACTIVE", activation_status="ACTIVE", runtime_status="IMPLEMENTED_IN_LITE",
                review_status="HUMAN_APPROVED", requirements_are_design_only=False, blockers=[])
    assert not validator.is_valid(item)


def test_dependency_strength_lists_are_consistent_and_sparse():
    for item in taxonomy().values():
        mapping = item["dependency_strengths"]
        for strength, field in (("PRIMARY", "primary_dependencies"),
                                ("SECONDARY", "secondary_dependencies"),
                                ("OPTIONAL", "optional_dependencies")):
            assert set(item[field]) == {d for d, status in mapping.items() if status == strength}
        assert not (set(item["primary_dependencies"]) & set(item["secondary_dependencies"]))
        assert len(item["primary_dependencies"]) < len(DIMENSIONS)


def test_all_diagnostic_evidence_gate_refs_resolve_or_are_explicitly_unavailable():
    known_d = {read(p)["id"] for p in (K / "diagnostics/catalog").glob("*.json")}
    known_e = {x["evidence_id"] for x in read(K / "diagnostics/EVIDENCE_DEPENDENCY_CATALOG.json")["evidence_families"]}
    known_g = {x["gate_id"] for x in read(K / "gates/index.json")["gates"]}
    assert len(known_d) == 61 and len(known_g) == 6
    for item in taxonomy().values():
        assert set(item["required_diagnostics"] + item["optional_diagnostics"] + item["context_diagnostics"] + item["quarantined_diagnostics"]) <= known_d
        assert set(item["required_evidence_families"] + item["optional_evidence_families"]) <= known_e
        assert all(x["status"] == "UNAVAILABLE" and x["reason"] for x in item["future_evidence_dependencies"])
        assert set(item["required_gates"]) == known_g
        assert item["gate_applicability_status"] == "UNRESOLVED_UNTIL_APPROVED_POLICY_AND_ACTION_CONTEXT"
        assert not (set(item["required_diagnostics"] + item["optional_diagnostics"]) & {"D35", "D57"})
        assert item["gate_fail_override_allowed"] is False
        assert item["broker_order_authority"] is False


def test_matrix_has_exactly_one_row_per_archetype_dimension_and_matches_artifacts():
    matrix = read(S / "STRATEGY_DEPENDENCY_MATRIX.json")
    rows = matrix["rows"]
    assert matrix["status"] == "DESIGN_ONLY_NOT_ACTIVE"
    assert (matrix["archetype_count"], matrix["dimension_count"], matrix["row_count"]) == (35, 10, 350)
    assert len(rows) == 350
    assert len({(r["strategy_archetype_id"], r["dependency_dimension"]) for r in rows}) == 350
    assert set(matrix["dimensions"]) == DIMENSIONS
    for row in rows:
        item = taxonomy()[row["strategy_archetype_id"]]
        assert row["primary_family"] == item["primary_family"]
        assert row["dependency_strength"] == item["dependency_strengths"][row["dependency_dimension"]]
        assert row["future_runtime_status"] == "NOT_IMPLEMENTED_IN_LITE"
        if row["dependency_strength"] == "NOT_REQUIRED":
            assert not (row["evidence_families"] or row["diagnostic_ids"] or row["unresolved_dependencies"])
        else:
            assert set(row["evidence_families"]) <= set(item["required_evidence_families"] + item["optional_evidence_families"])
            assert set(row["diagnostic_ids"]) <= set(item["required_diagnostics"] + item["optional_diagnostics"] + item["context_diagnostics"])
            assert row["unresolved_dependencies"]


def test_distinct_analysis_philosophies_and_long_term_decomposition():
    t = taxonomy()
    fi, pre = t["FUNDAMENTAL_INFLECTION"], t["PRE_BREAKOUT_ACCUMULATION"]
    assert fi["dependency_strengths"]["FUNDAMENTALS"] == "PRIMARY"
    assert fi["dependency_strengths"]["TECHNICALS"] == "OPTIONAL"
    assert pre["dependency_strengths"]["TECHNICALS"] == "PRIMARY"
    assert pre["dependency_strengths"]["FLOW"] == "PRIMARY"
    assert fi["analysis_stages"] != pre["analysis_stages"]
    turn, mid = t["TURNAROUND_RECOVERY"], t["MID_TERM_COMPOUNDER"]
    assert turn["analysis_stages"][0] == "problem identified"
    assert mid["analysis_stages"][0] == "industry runway"
    assert turn["dependency_strengths"]["BALANCE_SHEET_CASH_FLOW"] == "PRIMARY"
    assert mid["dependency_strengths"]["MANAGEMENT_GOVERNANCE"] == "SECONDARY"
    structural = [x for x in t.values() if x["primary_family"] == "FAMILY_F_STRUCTURAL_GROWTH"]
    assert len(structural) >= 5
    assert "LONG_TERM" not in t
    assert all(x["horizon_authority"] == "INTENDED_ONLY_NOT_VALIDATED" for x in t.values())


def test_nonactive_authority_and_legacy_provenance_are_conservative():
    for item in taxonomy().values():
        assert item["authority_status"] == "PROPOSED_NOT_ACTIVE"
        assert item["lifecycle"] == "EXTRACTED_DRAFT"
        assert item["activation_status"] == "NOT_ACTIVE"
        assert item["runtime_status"] == "NOT_IMPLEMENTED_IN_LITE"
        assert item["requirements_are_design_only"] is True
        assert item["blockers"]
        assert any(p["origin_kind"] == "TASK_008_USER_BRIEF" for p in item["provenance"])
        if item["legacy_sources"]:
            assert item["legacy_commit"] == SHA
            assert item["authority_origin"] == "COMPOSITE_DERIVATION"
            assert all(any(p["origin_kind"] == "LEGACY_READ_ONLY" and p["reference"] == source
                           for p in item["provenance"]) for source in item["legacy_sources"])
        else:
            assert item["legacy_commit"] is None
            assert item["authority_origin"] == "FOUNDER_DESIGN"
    assert read(K / "diagnostics/catalog/D35_vwap_value_area.json")["status"] == "QUARANTINED"
    assert read(K / "diagnostics/catalog/D57_post_news_reaction.json")["status"] == "QUARANTINED"


def test_task007_mapping_covers_six_and_transfers_no_authority():
    prior = {x["strategy_id"] for x in read(S / "registry.json")["entries"]}
    mapping = read(S / "TASK007_TO_TAXONOMY_MAP.json")
    assert {x["prior_strategy_id"] for x in mapping["entries"]} == prior
    assert mapping["authority_transfer_default"] is False
    for x in mapping["entries"]:
        assert x["mapping_type"] in {"EXACT", "UMBRELLA", "PARTIAL", "RESEARCH_CONTEXT"}
        assert set(x["new_archetype_ids"]) <= set(taxonomy())
        assert x["prior_authority_transfers"] is False and x["limitations"]
    assert {x["mapping_type"] for x in mapping["entries"]} >= {"EXACT", "UMBRELLA", "PARTIAL", "RESEARCH_CONTEXT"}


def test_overlap_blocks_naive_independence_and_confluence_has_no_number():
    overlap = read(S / "STRATEGY_OVERLAP_MATRIX.json")
    confluence = read(S / "STRATEGY_CONFLUENCE_MODEL.json")
    assert set(overlap["categories"]) == {"INDEPENDENT", "PARTIALLY_OVERLAPPING", "HIGHLY_OVERLAPPING", "SAME_FAMILY_CORRELATED", "UNRESOLVED"}
    assert overlap["pair_population"] == "RULE_BASED_NOT_ENUMERATED_35x35"
    assert overlap["no_naive_independent_confirmation_count"] is True
    assert overlap["source_lineage_scope"].endswith("EXCLUDE_SHARED_TAXONOMY_DESIGN_PROVENANCE")
    assert overlap["numeric_overlap_threshold"] is None
    assert [r["rule_id"] for r in overlap["rules_in_precedence_order"]] == [
        "R1_IDENTITY", "R2_SHARED_EVENT_OR_POLICY", "R3_IDENTICAL_DEPENDENCY_LINEAGE",
        "R4_SAME_PRIMARY_FAMILY", "R5_CROSS_FAMILY_SHARED_INPUT", "R6_CROSS_FAMILY_DISTINCT",
        "R7_INCOMPLETE_METADATA",
    ]
    assert all(not r["independent_confirmation_allowed"] for r in overlap["rules_in_precedence_order"] if r["category"] != "INDEPENDENT")
    assert confluence["numeric_activation_threshold"] is confluence["numeric_strategy_threshold"] is confluence["universal_strategy_score"] is None
    assert confluence["count_above_threshold_formula_allowed"] is False
    assert confluence["naive_match_count_as_independent_allowed"] is False
    assert {x["state"] for x in confluence["states"]} == {"NO_CONFLUENCE", "SINGLE_STRATEGY", "MULTI_STRATEGY_SAME_FAMILY", "CROSS_FAMILY_CONFLUENCE", "HIGH_DIVERSITY_CONFLUENCE", "UNRESOLVED"}
    assert confluence["global_hsi_score"]["policy_id"] == "decision-score-v1"
    assert confluence["global_hsi_score"]["replaced_by_strategy_score"] is False
    assert confluence["archetype_specific_score"]["status"] == "FUTURE_NOT_IMPLEMENTED"
    assert confluence["gate_fail_override_allowed"] is False
    assert confluence["broker_order_authority"] is False
    assert confluence["unknown_strategy_result"] == read(S / "registry.json")["unknown_strategy_result"] == "STRATEGY_UNAVAILABLE"


def test_no_runtime_strategy_scoring_or_provider_added():
    assert not any(T.glob("*.py"))
    assert not (S / "strategy_score_engine.py").exists()
    assert not (S / "confluence_engine.py").exists()
    assert all(p.suffix == ".json" for p in T.iterdir())
