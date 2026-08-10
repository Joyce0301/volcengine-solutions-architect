import hashlib
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
FORWARD = ROOT / "tests" / "forward"


class ForwardProvenanceTests(unittest.TestCase):
    def test_manifest_hashes_match_current_fixtures(self):
        manifest = (FORWARD / "collection-provenance.md").read_text(encoding="utf-8")
        fixtures = (
            "ai-agent.md",
            "cloud-native.md",
            "intelligent-service.md",
            "media.md",
            "realtime-data.md",
            "regulated-finance.md",
            "interview-behavior.json",
        )
        for fixture in fixtures:
            digest = hashlib.sha256((FORWARD / fixture).read_bytes()).hexdigest()
            with self.subTest(fixture=fixture):
                self.assertIn(f"`{digest}`", manifest)


if __name__ == "__main__":
    unittest.main()
