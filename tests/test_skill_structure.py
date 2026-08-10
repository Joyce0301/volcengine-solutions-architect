import re
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

EXPECTED_SKILLS = {
    "design-volcengine-architecture",
    "interview-volcengine-requirements",
    "route-volcengine-architecture",
    "select-volcengine-products",
    "design-volcengine-ai-agent",
    "design-volcengine-cloud-native",
    "design-volcengine-data-analytics",
    "design-volcengine-database-storage",
    "design-volcengine-media-edge",
    "design-volcengine-network-security",
    "render-volcengine-architecture",
    "write-volcengine-architecture-report",
    "coordinate-volcengine-architecture-roles",
}


class SkillStructureTests(unittest.TestCase):
    def test_plugin_and_skills_are_root_level(self):
        self.assertTrue((ROOT / ".codex-plugin" / "plugin.json").is_file())
        self.assertTrue(SKILLS.is_dir())
        self.assertFalse((ROOT / "volcengine-architecture").exists())
        plugin = json.loads(
            (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual("./skills/", plugin["skills"])

    def test_every_promoted_capability_is_a_discoverable_skill(self):
        actual = {path.name for path in SKILLS.iterdir() if path.is_dir()}
        self.assertEqual(EXPECTED_SKILLS, actual)
        for name in EXPECTED_SKILLS:
            skill_file = SKILLS / name / "SKILL.md"
            with self.subTest(skill=name):
                self.assertTrue(skill_file.is_file())
                text = skill_file.read_text(encoding="utf-8")
                self.assertRegex(text, rf"(?m)^name:\s*{re.escape(name)}\s*$")
                self.assertRegex(text, r"(?m)^description:\s*.+$")
                if name != "design-volcengine-architecture":
                    self.assertIn("## Standalone invocation", text)

    def test_orchestrator_has_no_private_markdown_references(self):
        reference_dir = SKILLS / "design-volcengine-architecture" / "references"
        self.assertFalse(reference_dir.exists())

    def test_orchestrator_routes_to_every_promoted_skill(self):
        orchestrator = (
            SKILLS / "design-volcengine-architecture" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for name in EXPECTED_SKILLS - {"design-volcengine-architecture"}:
            with self.subTest(skill=name):
                self.assertIn(f"${name}", orchestrator)


if __name__ == "__main__":
    unittest.main()
