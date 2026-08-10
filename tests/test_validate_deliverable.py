import importlib.util
from pathlib import Path
import unittest


VALIDATOR_PATH = (
    Path(__file__).parents[1]
    / "volcengine-architecture"
    / "skills"
    / "design-volcengine-architecture"
    / "scripts"
    / "validate-deliverable.py"
)

spec = importlib.util.spec_from_file_location("validate_deliverable", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
validate_markdown = validator.validate_markdown


VALID_MARKDOWN = """## Requirements gap check

- Facts: test fixture.
- Open items: no critical open items.
- Assumptions: test fixture.

## Executive summary
Summary.

## Known facts, assumptions, and open items
No critical open items.

```yaml
routing:
  scenario_labels: [CLOUD_NATIVE]
  quality_labels: [HIGH_AVAILABILITY]
  constraint_labels: [PRIVATE_NETWORK]
  product_families: [compute-cloud-native]
  roles: [requirements-analyst]
  execution_mode: serial
  rationale: [test fixture]
```

## Architecture decisions
Decisions.

## Logical architecture
```mermaid
graph TD
A[云服务器 ECS]-->B[Application]
```

## Deployment topology
Topology.

## End-to-end data flow
Flow.

## Volcengine product mapping
| Architecture capability | Recommended Volcengine product | Responsibility | Why it fits | Alternative | Switch condition | Evidence |
|---|---|---|---|---|---|---|
| Compute | 云服务器 ECS | Runs application workloads | Supports the existing operating model | 容器服务 | Use container orchestration when Kubernetes APIs are required | https://www.volcengine.com/docs/6396 Retrieved: 2026-08-08 |

## Non-functional design
Design.

## Implementation roadmap
Roadmap.

## Risk and validation plan
Plan.

## Official evidence and freshness
https://www.volcengine.com/docs/6396 Retrieved: 2026-08-08

## Completeness score
Production readiness: NOT READY
Requirements: 2
Architecture: 2
Security: 2
Reliability: 2
Cost: 2
Evidence: 2
"""


class ValidateDeliverableTests(unittest.TestCase):
    def test_valid_complete_deliverable_has_no_errors(self):
        assert validate_markdown(VALID_MARKDOWN) == []

    def test_requires_requirements_gap_check_as_first_visible_content(self):
        text = VALID_MARKDOWN.replace(
            "## Requirements gap check",
            "# Architecture proposal\n\n## Requirements gap check",
            1,
        )
        assert "first visible content must be: ## Requirements gap check" in validate_markdown(text)

    def test_requires_exactly_one_production_readiness_line(self):
        without_readiness = VALID_MARKDOWN.replace("Production readiness: NOT READY\n", "")
        assert (
            "expected exactly one Production readiness line with READY or NOT READY"
            in validate_markdown(without_readiness)
        )

        duplicated_readiness = VALID_MARKDOWN.replace(
            "Production readiness: NOT READY",
            "Production readiness: NOT READY\nProduction readiness: NOT READY",
        )
        assert (
            "expected exactly one Production readiness line with READY or NOT READY"
            in validate_markdown(duplicated_readiness)
        )

    def test_reports_missing_required_section(self):
        text = VALID_MARKDOWN.replace("## Risk and validation plan", "## Removed")
        assert "missing section: Risk and validation plan" in validate_markdown(text)

    def test_requires_mermaid_or_explicit_diagram_degradation(self):
        text = VALID_MARKDOWN.replace(
            "```mermaid\ngraph TD\nA[云服务器 ECS]-->B[Application]\n```",
            "no diagram",
        )
        assert "missing Mermaid diagram or diagram degradation notice" in validate_markdown(text)

    def test_ready_requires_full_scores(self):
        text = VALID_MARKDOWN.replace("Production readiness: NOT READY", "Production readiness: READY")
        text = text.replace("Evidence: 2", "Evidence: 1")
        assert "READY requires all completeness scores to equal 2" in validate_markdown(text)

    def test_ready_allows_explicitly_negated_critical_open_items(self):
        text = VALID_MARKDOWN.replace("Production readiness: NOT READY", "Production readiness: READY")
        assert validate_markdown(text) == []

    def test_ready_rejects_affirmative_critical_open_item(self):
        text = VALID_MARKDOWN.replace("Production readiness: NOT READY", "Production readiness: READY")
        text = text.replace("No critical open items.", "Critical open item: recovery target unknown.")
        assert "READY is incompatible with a critical open item" in validate_markdown(text)

    def test_dynamic_fact_requires_official_url_and_date(self):
        text = VALID_MARKDOWN + "\nThe SLA is 99.95%.\n"
        assert "dynamic fact lacks nearby official evidence and retrieval date" in validate_markdown(text)

    def test_https_url_does_not_trigger_tps_detection(self):
        text = VALID_MARKDOWN + "\nOfficial discovery: https://www.volcengine.com/docs/6401.\n"
        assert validate_markdown(text) == []

    def test_plural_dynamic_terms_require_evidence(self):
        text = VALID_MARKDOWN + "\nProduction regions, prices, SLAs, and quotas are ready.\n"
        assert "dynamic fact lacks nearby official evidence and retrieval date" in validate_markdown(text)

    def test_product_mapping_evidence_requires_retrieval_date(self):
        text = VALID_MARKDOWN.replace(
            "| Compute | 云服务器 ECS | Runs application workloads | Supports the existing operating model | 容器服务 | Use container orchestration when Kubernetes APIs are required | https://www.volcengine.com/docs/6396 Retrieved: 2026-08-08 |",
            "| Compute | 云服务器 ECS | Runs application workloads | Supports the existing operating model | 容器服务 | Use container orchestration when Kubernetes APIs are required | https://www.volcengine.com/docs/6396 |",
        )
        assert "product mapping evidence lacks official URL and retrieval date" in validate_markdown(text)

    def test_product_mapping_rejects_generic_only_product_names(self):
        text = VALID_MARKDOWN.replace(
            "| Compute | 云服务器 ECS | Runs application workloads | Supports the existing operating model | 容器服务 | Use container orchestration when Kubernetes APIs are required | https://www.volcengine.com/docs/6396 Retrieved: 2026-08-08 |",
            "| Compute | Managed compute | Runs application workloads | Supports the existing operating model | Container platform | Use container orchestration when Kubernetes APIs are required | https://www.volcengine.com/docs/6396 Retrieved: 2026-08-08 |",
        )
        assert "product mapping lacks a concrete Volcengine product" in validate_markdown(text)

    def test_product_mapping_rejects_alias_without_canonical_name(self):
        text = VALID_MARKDOWN.replace(
            "| Compute | 云服务器 ECS |",
            "| Compute | 云服务器 ECS + IAM |",
        )
        assert (
            "product mapping uses alias without canonical product name: IAM"
            in validate_markdown(text)
        )

    def test_product_mapping_rejects_abbreviated_second_product(self):
        text = VALID_MARKDOWN.replace(
            "| Compute | 云服务器 ECS |",
            "| Compute | 云数据库 PostgreSQL 版或 MySQL 版 |",
        )
        assert (
            "product mapping uses alias without canonical product name: MySQL 版"
            in validate_markdown(text)
        )

    def test_product_mapping_allows_alias_appended_to_its_canonical_name(self):
        text = VALID_MARKDOWN.replace(
            "| Compute | 云服务器 ECS |",
            "| Compute | 云服务器 ECS (ECS) |",
        )
        assert validate_markdown(text) == []

        text = VALID_MARKDOWN.replace(
            "| Compute | 云服务器 ECS |",
            "| Compute | 密钥管理系统 KMS |",
        ).replace(
            "A[云服务器 ECS]-->B[Application]",
            "A[密钥管理系统]-->B[Application]",
        )
        assert validate_markdown(text) == []

    def test_product_mapping_requires_at_least_one_product_row(self):
        text = VALID_MARKDOWN.replace(
            "| Compute | 云服务器 ECS | Runs application workloads | Supports the existing operating model | 容器服务 | Use container orchestration when Kubernetes APIs are required | https://www.volcengine.com/docs/6396 Retrieved: 2026-08-08 |",
            "",
        )
        assert "product mapping has no concrete product rows" in validate_markdown(text)

    def test_product_mapping_requires_product_responsibility(self):
        text = VALID_MARKDOWN.replace(
            "| Compute | 云服务器 ECS | Runs application workloads | Supports the existing operating model |",
            "| Compute | 云服务器 ECS | | Supports the existing operating model |",
        )
        assert "product mapping missing Responsibility" in validate_markdown(text)

    def test_product_mapping_requires_selection_rationale(self):
        text = VALID_MARKDOWN.replace(
            "| Runs application workloads | Supports the existing operating model | 容器服务 |",
            "| Runs application workloads | | 容器服务 |",
        )
        assert "product mapping missing Why it fits" in validate_markdown(text)

    def test_product_mapping_requires_alternative(self):
        text = VALID_MARKDOWN.replace(
            "| Supports the existing operating model | 容器服务 | Use container orchestration",
            "| Supports the existing operating model | | Use container orchestration",
        )
        assert "product mapping missing Alternative" in validate_markdown(text)

    def test_product_mapping_requires_switch_condition(self):
        text = VALID_MARKDOWN.replace(
            "| 容器服务 | Use container orchestration when Kubernetes APIs are required |",
            "| 容器服务 | |",
        )
        assert "product mapping missing Switch condition" in validate_markdown(text)

    def test_mermaid_products_must_be_recommended_in_product_mapping(self):
        text = VALID_MARKDOWN.replace(
            "A[云服务器 ECS]-->B[Application]",
            "A[对象存储 TOS]-->B[Application]",
        )
        assert "diagram product is absent from recommended product mapping: 对象存储 TOS" in validate_markdown(text)

    def test_mermaid_alias_resolves_to_canonical_product(self):
        text = VALID_MARKDOWN.replace(
            "A[云服务器 ECS]-->B[Application]",
            "A[TOS]-->B[Application]",
        )
        assert "diagram product is absent from recommended product mapping: 对象存储 TOS" in validate_markdown(text)

    def test_decision_products_must_be_recommended_in_product_mapping(self):
        text = VALID_MARKDOWN.replace(
            "## Architecture decisions\nDecisions.",
            "## Architecture decisions\nUse 对象存储 TOS for durable artifacts.",
        )
        assert "architecture decisions product is absent from recommended product mapping: 对象存储 TOS" in validate_markdown(text)

    def test_decision_alias_resolves_to_canonical_product(self):
        text = VALID_MARKDOWN.replace(
            "## Architecture decisions\nDecisions.",
            "## Architecture decisions\nUse TOS for durable artifacts.",
        )
        assert "architecture decisions product is absent from recommended product mapping: 对象存储 TOS" in validate_markdown(text)

    def test_decision_table_alternatives_do_not_count_as_active_products(self):
        text = VALID_MARKDOWN.replace(
            "## Architecture decisions\nDecisions.",
            """## Architecture decisions
| Decision | Rationale | Alternative | Reason not selected |
| --- | --- | --- | --- |
| Use 云服务器 ECS | Fits the operating model | 对象存储 TOS | It is not a compute service |""",
        )
        assert validate_markdown(text) == []

    def test_flow_products_must_be_recommended_in_product_mapping(self):
        text = VALID_MARKDOWN.replace(
            "## End-to-end data flow\nFlow.",
            "## End-to-end data flow\nWrite durable artifacts to 对象存储 TOS.",
        )
        assert "end-to-end data flow product is absent from recommended product mapping: 对象存储 TOS" in validate_markdown(text)

    def test_flow_alias_resolves_to_canonical_product(self):
        text = VALID_MARKDOWN.replace(
            "## End-to-end data flow\nFlow.",
            "## End-to-end data flow\nWrite durable artifacts to TOS.",
        )
        assert "end-to-end data flow product is absent from recommended product mapping: 对象存储 TOS" in validate_markdown(text)

    def test_alias_does_not_match_inside_an_english_word(self):
        text = VALID_MARKDOWN.replace(
            "## End-to-end data flow\nFlow.",
            "## End-to-end data flow\nClass entry is synchronous.",
        )
        assert validate_markdown(text) == []

    def test_mermaid_rejects_unresolved_generic_component(self):
        text = VALID_MARKDOWN.replace(
            "A[云服务器 ECS]-->B[Application]",
            "A[数据库]-->B[Application]",
        )
        assert "diagram contains unresolved generic component: 数据库" in validate_markdown(text)

    def test_overlapping_product_names_are_checked_at_distinct_diagram_nodes(self):
        text = VALID_MARKDOWN.replace(
            "A[云服务器 ECS]-->B[Application]",
            "A[火山方舟]-->B[火山方舟语音模型]",
        ).replace(
            "| Compute | 云服务器 ECS |",
            "| Compute | 火山方舟语音模型 |",
        )
        assert "diagram product is absent from recommended product mapping: 火山方舟" in validate_markdown(text)

    def test_unresolved_architecture_gap_requires_assumption_and_switch_condition(self):
        text = VALID_MARKDOWN.replace(
            "- Facts: test fixture.\n- Open items: no critical open items.\n- Assumptions: test fixture.",
            "Known facts:\n- test fixture.\nArchitecture-changing gaps:\n- Recovery objective is unknown.\nAssumptions if unanswered:\n- none.",
        )
        assert "unresolved architecture gap requires Assumption and Switch condition" in validate_markdown(text)

    def test_each_unresolved_gap_requires_its_own_assumption_and_switch_condition(self):
        text = VALID_MARKDOWN.replace(
            "- Facts: test fixture.\n- Open items: no critical open items.\n- Assumptions: test fixture.",
            "Known facts:\n- test fixture.\nArchitecture-changing gaps:\n- Recovery objective is unknown.\n- Data sensitivity is unknown.\nAssumptions if unanswered:\n- Assumption: recovery uses the default target.\n- Switch condition: If the target changes, change recovery topology.",
        )
        assert "each unresolved architecture gap requires its own Assumption and Switch condition" in validate_markdown(text)

    def test_requires_routing_record(self):
        text = VALID_MARKDOWN.replace(
            "```yaml\nrouting:\n  scenario_labels: [CLOUD_NATIVE]\n  quality_labels: [HIGH_AVAILABILITY]\n  constraint_labels: [PRIVATE_NETWORK]\n  product_families: [compute-cloud-native]\n  roles: [requirements-analyst]\n  execution_mode: serial\n  rationale: [test fixture]\n```\n\n",
            "",
        )
        assert "missing routing record before architecture decisions" in validate_markdown(text)

    def test_routing_record_must_precede_architecture_decisions(self):
        routing = "```yaml\nrouting:\n  scenario_labels: [CLOUD_NATIVE]\n  quality_labels: [HIGH_AVAILABILITY]\n  constraint_labels: [PRIVATE_NETWORK]\n  product_families: [compute-cloud-native]\n  roles: [requirements-analyst]\n  execution_mode: serial\n  rationale: [test fixture]\n```\n\n"
        text = VALID_MARKDOWN.replace(routing, "")
        text = text.replace("## Architecture decisions\nDecisions.", "## Architecture decisions\nDecisions.\n\n" + routing)
        assert "missing routing record before architecture decisions" in validate_markdown(text)


if __name__ == "__main__":
    unittest.main()
