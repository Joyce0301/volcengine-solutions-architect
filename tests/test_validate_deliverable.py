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


VALID_MARKDOWN = """# Architecture proposal

## Executive summary
Summary.

## Known facts, assumptions, and open items
No critical open items.

## Architecture decisions
Decisions.

## Logical architecture
```mermaid
graph TD
A-->B
```

## Deployment topology
Topology.

## End-to-end data flow
Flow.

## Volcengine product mapping
| Architecture capability | Recommended Volcengine product | Why it fits | Alternative | Switch condition | Evidence |
|---|---|---|---|---|---|
| Compute | ECS | General compute | VKE | Container orchestration needed | Official documentation |

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

    def test_reports_missing_required_section(self):
        text = VALID_MARKDOWN.replace("## Risk and validation plan", "## Removed")
        assert "missing section: Risk and validation plan" in validate_markdown(text)

    def test_requires_mermaid_or_explicit_diagram_degradation(self):
        text = VALID_MARKDOWN.replace("```mermaid\ngraph TD\nA-->B\n```", "no diagram")
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


if __name__ == "__main__":
    unittest.main()
