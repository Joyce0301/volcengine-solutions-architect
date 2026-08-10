import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
SKILL = SKILLS / "design-volcengine-architecture"


class ReportContractTests(unittest.TestCase):
    def test_skill_requires_report_contract_and_default_path(self):
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        contract_text = (SKILLS / "write-volcengine-architecture-report" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("$write-volcengine-architecture-report", skill_text)
        self.assertIn("reports/volcengine-architecture-report.md", skill_text)
        self.assertIn("reports/volcengine-architecture-report.md", contract_text)

    def test_output_contract_identifies_report(self):
        output_text = (SKILLS / "render-volcengine-architecture" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("self-contained Markdown report", output_text)


if __name__ == "__main__":
    unittest.main()
