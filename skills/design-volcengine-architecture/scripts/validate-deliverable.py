#!/usr/bin/env python3
"""Validate the required structure of a Volcengine architecture deliverable."""

import argparse
import json
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
PRODUCT_REGISTRY_PATH = (
    Path(__file__).resolve().parents[2]
    / "select-volcengine-products"
    / "product-registry.json"
)


def load_product_registry() -> tuple[dict[str, object], ...]:
    registry = json.loads(PRODUCT_REGISTRY_PATH.read_text(encoding="utf-8"))
    return tuple(registry["products"])


PRODUCT_REGISTRY = load_product_registry()
CONCRETE_PRODUCT_NAMES = tuple(product["name"] for product in PRODUCT_REGISTRY)
GENERIC_COMPONENT_LABELS = (
    "数据库",
    "缓存",
    "对象存储",
    "消息队列",
    "容器平台",
    "database",
    "cache",
    "object storage",
    "message queue",
    "container platform",
)


def alias_pattern(alias: str) -> str:
    escaped = re.escape(alias.casefold())
    return rf"(?<![a-z0-9]){escaped}(?![a-z0-9])"


def mentioned_products(text: str) -> tuple[str, ...]:
    folded = text.casefold()
    candidates: list[tuple[int, int, str]] = []
    for product in PRODUCT_REGISTRY:
        name = str(product["name"])
        aliases = product.get("consistency_aliases", product.get("aliases", []))
        for index, label in enumerate((name, *aliases)):
            pattern = re.escape(str(label).casefold()) if index == 0 else alias_pattern(str(label))
            candidates.extend(
                (match.start(), match.end(), name)
                for match in re.finditer(pattern, folded)
            )

    accepted: list[tuple[int, int, str]] = []
    for start, end, name in sorted(candidates, key=lambda item: (item[0], item[0] - item[1])):
        if any(start < accepted_end and end > accepted_start for accepted_start, accepted_end, _ in accepted):
            continue
        accepted.append((start, end, name))

    return tuple(dict.fromkeys(name for _, _, name in accepted))


def aliases_without_canonical_name(text: str) -> tuple[str, ...]:
    folded = text.casefold()
    invalid: list[str] = []
    canonical_spans = [
        (match.start(), match.end())
        for name in CONCRETE_PRODUCT_NAMES
        for match in re.finditer(re.escape(name.casefold()), folded)
    ]
    for product in PRODUCT_REGISTRY:
        product_name = str(product["name"])
        product_has_canonical_name = product_name.casefold() in folded
        for alias in product.get("aliases", []):
            for match in re.finditer(alias_pattern(str(alias)), folded):
                if not any(
                    start <= match.start() and match.end() <= end
                    for start, end in canonical_spans
                ) and not product_has_canonical_name:
                    invalid.append(str(alias))
                    break
    return tuple(dict.fromkeys(invalid))


def section_body(text: str, heading: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def active_decision_text(text: str) -> str:
    """Return decision prose and active table columns, excluding alternatives."""
    active_lines: list[str] = []
    for line in section_body(text, "Architecture decisions").splitlines():
        if not line.lstrip().startswith("|"):
            active_lines.append(line)
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or all(re.fullmatch(r"-+", cell) for cell in cells):
            continue
        active_lines.append(" | ".join(cells[:2]))
    return "\n".join(active_lines)


def first_visible_line(text: str) -> str:
    remainder = text
    while True:
        stripped = remainder.lstrip()
        if stripped.startswith("<!--"):
            end = stripped.find("-->")
            if end == -1:
                return stripped.splitlines()[0] if stripped.splitlines() else ""
            remainder = stripped[end + 3 :]
            continue
        return stripped.splitlines()[0] if stripped.splitlines() else ""


def validate_markdown(text: str) -> list[str]:
    errors: list[str] = []
    if first_visible_line(text) != "## Requirements gap check":
        errors.append("first visible content must be: ## Requirements gap check")

    gap_match = re.search(
        r"^Architecture-changing gaps:\s*\n(.*?)(?=^(?:Assumptions if unanswered:|##\s))",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if gap_match:
        gap_text = gap_match.group(1).strip()
        no_gap = re.fullmatch(r"(?:-\s*)?(?:none|无)[。.]?", gap_text, re.IGNORECASE)
        if gap_text and not no_gap:
            gap_count = len(re.findall(r"^\s*-\s+\S", gap_text, re.MULTILINE)) or 1
            assumption_count = len(
                re.findall(r"^\s*(?:-\s*)?Assumption:", text, re.MULTILINE)
            )
            switch_count = len(
                re.findall(r"^\s*(?:-\s*)?Switch condition:", text, re.MULTILINE)
            )
            if assumption_count == 0 or switch_count == 0:
                errors.append(
                    "unresolved architecture gap requires Assumption and Switch condition"
                )
            elif assumption_count < gap_count or switch_count < gap_count:
                errors.append(
                    "each unresolved architecture gap requires its own Assumption and Switch condition"
                )

    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", text, re.MULTILINE):
            errors.append(f"missing section: {section}")

    architecture_match = re.search(r"^##\s+Architecture decisions\s*$", text, re.MULTILINE)
    architecture_start = architecture_match.start() if architecture_match else len(text)
    pre_architecture = text[:architecture_start]
    if not re.search(r"```(?:yaml|yml)?\s*\nrouting:\s*\n", pre_architecture, re.IGNORECASE):
        errors.append("missing routing record before architecture decisions")

    mapping_header = (
        "| Architecture capability | Recommended Volcengine product | Responsibility | Why it fits "
        "| Alternative | Switch condition | Evidence |"
    )
    if mapping_header not in text:
        errors.append("missing exact product mapping table header")
    else:
        mapping_section = text.split(mapping_header, 1)[1].split("\n## ", 1)[0]
        recommended_products: list[str] = []
        for line in mapping_section.splitlines():
            if not line.startswith("|") or re.fullmatch(r"\|\s*-+.*", line):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) >= 7:
                recommended_products.append(cells[1])
                if not cells[2]:
                    errors.append("product mapping missing Responsibility")
                    break
                if not cells[3]:
                    errors.append("product mapping missing Why it fits")
                    break
                if not cells[4]:
                    errors.append("product mapping missing Alternative")
                    break
                if not cells[5]:
                    errors.append("product mapping missing Switch condition")
                    break
                recommended_product = cells[1]
                if not any(
                    name.casefold() in recommended_product.casefold()
                    for name in CONCRETE_PRODUCT_NAMES
                ):
                    errors.append("product mapping lacks a concrete Volcengine product")
                    break
                unsupported_aliases = aliases_without_canonical_name(recommended_product)
                if unsupported_aliases:
                    errors.append(
                        "product mapping uses alias without canonical product name: "
                        f"{unsupported_aliases[0]}"
                    )
                    break
                evidence = cells[-1]
                if "volcengine.com" not in evidence or not re.search(
                    r"(?:Retrieved:\s*|查询日期：)\d{4}-\d{2}-\d{2}", evidence
                ):
                    errors.append("product mapping evidence lacks official URL and retrieval date")
                    break

        if not recommended_products:
            errors.append("product mapping has no concrete product rows")

        diagram_text = "\n".join(
            match.group(1)
            for match in re.finditer(r"```mermaid\s*\n(.*?)```", text, re.IGNORECASE | re.DOTALL)
        )
        diagram_without_products = diagram_text.casefold()
        for product in sorted(CONCRETE_PRODUCT_NAMES, key=len, reverse=True):
            diagram_without_products = diagram_without_products.replace(product.casefold(), " ")
        for label in GENERIC_COMPONENT_LABELS:
            if label.casefold() in diagram_without_products:
                errors.append(f"diagram contains unresolved generic component: {label}")

        recommended_mentions = set(mentioned_products("\n".join(recommended_products)))
        for product in mentioned_products(active_decision_text(text)):
            if product not in recommended_mentions:
                errors.append(
                    "architecture decisions product is absent from recommended product mapping: "
                    f"{product}"
                )
        for product in mentioned_products(section_body(text, "End-to-end data flow")):
            if product not in recommended_mentions:
                errors.append(
                    "end-to-end data flow product is absent from recommended product mapping: "
                    f"{product}"
                )
        for product in mentioned_products(diagram_text):
            if product not in recommended_mentions:
                errors.append(
                    f"diagram product is absent from recommended product mapping: {product}"
                )

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

    readiness_matches = re.findall(r"^Production readiness:\s*(READY|NOT READY)\s*$", text, re.MULTILINE)
    if len(readiness_matches) != 1:
        errors.append("expected exactly one Production readiness line with READY or NOT READY")

    if readiness_matches == ["READY"]:
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
