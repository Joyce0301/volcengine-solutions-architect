import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = (
    ROOT
    / "skills"
    / "design-volcengine-architecture"
    / "scripts"
    / "validate-deliverable.py"
)

spec = importlib.util.spec_from_file_location("forward_report_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ForwardReportTests(unittest.TestCase):
    def test_forward_architecture_reports_pass_current_contract(self):
        reports = sorted((ROOT / "tests" / "forward").glob("*.md"))
        reports = [report for report in reports if report.name != "collection-provenance.md"]
        self.assertEqual(6, len(reports))

        failures = {}
        for report in reports:
            errors = validator.validate_markdown(report.read_text(encoding="utf-8"))
            if errors:
                failures[report.name] = errors

        self.assertEqual({}, failures)


if __name__ == "__main__":
    unittest.main()
