import unittest
from pathlib import Path
import json
import importlib.util
import re


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "volcengine-architecture" / "skills" / "design-volcengine-architecture"
VALIDATOR_PATH = SKILL / "scripts" / "validate-deliverable.py"

validator_spec = importlib.util.spec_from_file_location("adaptive_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(validator_spec)
validator_spec.loader.exec_module(validator)


class AdaptiveInterviewContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        cls.intake_text = (SKILL / "references" / "intake-contract.md").read_text(
            encoding="utf-8"
        )
        cls.output_text = (SKILL / "references" / "architecture-output.md").read_text(
            encoding="utf-8"
        )

    def test_interview_asks_exactly_one_question_per_turn(self):
        self.assertIn("Ask exactly one question per assistant turn", self.skill_text)
        self.assertIn("Ask exactly one question per assistant turn", self.intake_text)

    def test_interview_is_adaptive_and_bounded(self):
        self.assertIn("hard ceiling of eight", self.skill_text)
        self.assertIn("no unresolved question can materially change", self.intake_text)
        self.assertNotIn("Ask at most two rounds", self.skill_text)
        self.assertNotIn("Ask at most two rounds", self.intake_text)

    def test_user_can_continue_with_explicit_assumptions(self):
        self.assertIn("proceed with defaults", self.skill_text)
        self.assertIn("Assumption:", self.intake_text)
        self.assertIn("Switch condition:", self.intake_text)

    def test_output_requires_concrete_product_responsibility(self):
        self.assertIn("concrete Volcengine product", self.output_text)
        self.assertIn(
            "| Architecture capability | Recommended Volcengine product | Responsibility | Why it fits | Alternative | Switch condition | Evidence |",
            self.output_text,
        )

    def test_product_registry_matches_domain_reference_names(self):
        registry = json.loads(
            (SKILL / "references" / "product-registry.json").read_text(encoding="utf-8")
        )
        registry_names = {product["name"] for product in registry["products"]}
        reference_names = set()
        for reference in (SKILL / "references").glob("*.md"):
            reference_names.update(
                match.group(1).strip()
                for match in re.finditer(
                    r"^\s*-\s+product_name:\s*(.+?)\s*$",
                    reference.read_text(encoding="utf-8"),
                    re.MULTILINE,
                )
            )
        self.assertEqual(reference_names, registry_names)

    def test_forward_conversation_scenarios(self):
        evidence = json.loads(
            (ROOT / "tests" / "forward" / "interview-behavior.json").read_text(
                encoding="utf-8"
            )
        )
        cases = {case["id"]: case for case in evidence["cases"]}

        vague = cases["vague_prompt_enters_single_question_interview"]["turns"]
        vague_reply = vague[-1]["content"]
        self.assertEqual("interview", vague[-1]["phase"])
        self.assertEqual(1, vague_reply.count("Question:"))
        self.assertEqual(1, vague_reply.count("？"))
        self.assertNotIn("## Executive summary", vague_reply)

        early = cases["user_proceeds_with_defaults"]["turns"]
        self.assertEqual(["user", "assistant", "user", "assistant"], [turn["role"] for turn in early])
        self.assertEqual("report", early[-1]["phase"])
        early_report = (ROOT / "tests" / "forward" / early[-1]["report_fixture"]).read_text(
            encoding="utf-8"
        )
        self.assertIn("Assumption:", early_report)
        self.assertIn("Switch condition:", early_report)
        self.assertEqual([], validator.validate_markdown(early_report))

        rich = cases["information_rich_prompt_skips_interview"]["turns"]
        self.assertNotIn("interview", [turn.get("phase") for turn in rich])
        rich_report = (ROOT / "tests" / "forward" / rich[-1]["report_fixture"]).read_text(
            encoding="utf-8"
        )
        self.assertEqual([], validator.validate_markdown(rich_report))


if __name__ == "__main__":
    unittest.main()
