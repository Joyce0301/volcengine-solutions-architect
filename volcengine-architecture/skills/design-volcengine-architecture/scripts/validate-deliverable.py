#!/usr/bin/env python3
"""Validate the required structure of a Volcengine architecture deliverable."""

import argparse
from pathlib import Path
import re


REQUIRED_SECTIONS = (
    "Executive summary",
    "Known facts, assumptions, and open items",
    "Architecture decisions",
    "Logical architecture",
    "Deployment topology",
    "End-to-end data flow",
    "Volcengine product mapping",
    "Non-functional design",
    "Implementation roadmap",
    "Risk and validation plan",
    "Official evidence and freshness",
    "Completeness score",
)
SCORE_NAMES = ("Requirements", "Architecture", "Security", "Reliability", "Cost", "Evidence")


def validate_markdown(text: str) -> list[str]:
    errors: list[str] = []
    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", text, re.MULTILINE):
            errors.append(f"missing section: {section}")

    architecture_match = re.search(r"^##\s+Architecture decisions\s*$", text, re.MULTILINE)
    architecture_start = architecture_match.start() if architecture_match else len(text)
    pre_architecture = text[:architecture_start]
    if not re.search(r"```(?:yaml|yml)?\s*\nrouting:\s*\n", pre_architecture, re.IGNORECASE):
        errors.append("missing routing record before architecture decisions")

    mapping_header = (
        "| Architecture capability | Recommended Volcengine product | Why it fits "
        "| Alternative | Switch condition | Evidence |"
    )
    if mapping_header not in text:
        errors.append("missing exact product mapping table header")
    else:
        mapping_section = text.split(mapping_header, 1)[1].split("\n## ", 1)[0]
        for line in mapping_section.splitlines():
            if not line.startswith("|") or re.fullmatch(r"\|\s*-+.*", line):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) >= 6:
                evidence = cells[-1]
                if "volcengine.com" not in evidence or not re.search(
                    r"(?:Retrieved:\s*|查询日期：)\d{4}-\d{2}-\d{2}", evidence
                ):
                    errors.append("product mapping evidence lacks official URL and retrieval date")
                    break

    if "```mermaid" not in text and "Diagram degradation:" not in text:
        errors.append("missing Mermaid diagram or diagram degradation notice")

    scores = {
        name: int(match.group(1))
        for name in SCORE_NAMES
        if (match := re.search(rf"^{name}:\s*([0-2])\s*$", text, re.MULTILINE))
    }
    for name in SCORE_NAMES:
        if name not in scores:
            errors.append(f"missing completeness score: {name}")

    if re.search(r"^Production readiness:\s*READY\s*$", text, re.MULTILINE):
        if len(scores) != len(SCORE_NAMES) or any(value != 2 for value in scores.values()):
            errors.append("READY requires all completeness scores to equal 2")
        text_without_negated_items = re.sub(
            r"\bno\s+critical\s+open\s+items?\b", "", text, flags=re.IGNORECASE
        )
        if re.search(r"critical open item", text_without_negated_items, re.IGNORECASE):
            errors.append("READY is incompatible with a critical open item")

    dynamic = re.compile(
        r"\bprices?\b|价格|\bSLAs?\b|\bquotas?\b|配额|\bregions?\b|地域|\bQPS\b|\bTPS\b|\d+(?:\.\d+)?%",
        re.IGNORECASE,
    )
    dated = re.compile(r"(?:Retrieved:\s*|查询日期：)\d{4}-\d{2}-\d{2}")
    for paragraph in re.split(r"\n\s*\n", text):
        if dynamic.search(paragraph):
            if "volcengine.com" not in paragraph or not dated.search(paragraph):
                errors.append("dynamic fact lacks nearby official evidence and retrieval date")
                break

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate one Volcengine architecture Markdown deliverable."
    )
    parser.add_argument("markdown_file", help="path to one UTF-8 Markdown file")
    args = parser.parse_args()

    errors = validate_markdown(Path(args.markdown_file).read_text(encoding="utf-8"))
    if not errors:
        print("VALID")
        return 0

    for error in errors:
        print(error)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
