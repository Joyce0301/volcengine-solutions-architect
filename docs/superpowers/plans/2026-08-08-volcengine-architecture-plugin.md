# Volcengine Architecture Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a portable Codex Plugin whose main Skill turns incomplete business requirements into evidence-backed architectures using the full Volcengine product portfolio.

**Architecture:** Package one orchestration Skill inside a Codex Plugin. Keep the workflow lean, place domain knowledge and stable contracts in progressively loaded references, express subagent roles as runtime contracts, and use a standard-library Python validator to enforce the final deliverable shape.

**Tech Stack:** Codex Plugin manifest, Codex Skill, Markdown, Mermaid, runtime subagent contracts, Python 3 standard library, `unittest`, official Volcengine web documentation.

## Global Constraints

- Target Codex natively; keep intake, role, routing, and output contracts platform-neutral.
- Cover AI/Agent, cloud native, big data, databases/storage, networking/security, media, and edge products.
- Begin with a requirements-gap list and ask only questions whose answers change product selection or topology.
- Ask at most two rounds of architecture-changing questions; convert remaining gaps into explicit assumptions and branches.
- Treat multi-agent execution as an optimization, never an installation prerequisite.
- Use official Volcengine evidence for product existence and critical capabilities.
- Verify price, region, specification, quota, SLA, version status, and promotion facts at runtime with retrieval dates.
- Never invent exact cost, SLA, region, quota, or specification data.
- Do not provision live cloud resources or generate Terraform in version one.
- Default architecture output is Markdown plus Mermaid.
- Do not claim production readiness while any critical completeness dimension is insufficient.
- Use only Python standard-library dependencies for the deliverable validator.

---

## File Map

```text
tests/
├── scenarios/architecture-scenarios.md
├── baselines/{ai-agent,cloud-native,realtime-data,media,intelligent-service,regulated-finance}.md
├── forward/{ai-agent,cloud-native,realtime-data,media,intelligent-service,regulated-finance}.md
└── test_validate_deliverable.py
volcengine-architecture/
├── .codex-plugin/plugin.json
└── skills/design-volcengine-architecture/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/
    │   ├── intake-contract.md
    │   ├── routing-matrix.md
    │   ├── architecture-output.md
    │   ├── product-catalog.md
    │   ├── ai-and-agent.md
    │   ├── compute-cloud-native.md
    │   ├── data-analytics.md
    │   ├── database-storage.md
    │   ├── networking-security.md
    │   ├── media-edge.md
    │   └── subagent-contracts.md
    └── scripts/validate-deliverable.py
```

The distributable boundary is `volcengine-architecture/`. Repository-level tests are authoring evidence and are not needed at runtime.

---

### Task 1: Establish skill-free baseline behavior

**Files:**
- Create: `tests/scenarios/architecture-scenarios.md`
- Create: `tests/baselines/ai-agent.md`
- Create: `tests/baselines/cloud-native.md`
- Create: `tests/baselines/realtime-data.md`
- Create: `tests/baselines/media.md`
- Create: `tests/baselines/intelligent-service.md`
- Create: `tests/baselines/regulated-finance.md`

**Interfaces:**
- Consumes: approved design spec.
- Produces: six frozen prompts and unassisted responses that expose failures before `SKILL.md` exists.

- [ ] **Step 1: Write the six scenario prompts**

Create `tests/scenarios/architecture-scenarios.md` with:

```markdown
# Architecture Scenarios

## ai-agent
我们有约 3 万份内部制度和产品文档，想做一个能回答问题并调用工单系统的企业助手。请基于火山引擎设计架构。

## cloud-native
把一个日活 300 万、晚间有突发流量的电商 API 迁到火山引擎，要求尽量少改代码。请给出架构。

## realtime-data
我们需要汇总 App 埋点、交易和设备事件，支持分钟级运营看板和次日复杂分析。请设计火山引擎方案。

## media
设计一套面向全国用户的教育直播与回放平台，需要连麦、转码、内容审核和弱网体验保障。

## intelligent-service
构建支持电话和在线渠道的智能客服，需要语音识别、语音合成、知识问答、转人工和经营分析。

## regulated-finance
某金融机构希望在火山引擎部署客户风险分析平台，数据敏感，要求专网接入、完整审计、同城容灾和异地备份。
```

- [ ] **Step 2: Dispatch fresh agents without the new Skill**

For each scenario, dispatch a fresh agent with the fixed prefix below followed by the complete literal prompt under the matching heading created in Step 1:

```text
请直接完成下面的用户请求。当前没有可用的专用火山引擎架构 Skill。不要查看工作区中的设计文档或其他测试输出。

```

Save each raw response under `tests/baselines/<scenario>.md`.

- [ ] **Step 3: Score measured baseline gaps**

Append this exact checklist to each file:

```markdown
## Baseline observations
- Requirements gap list before solution: PASS|FAIL
- Only architecture-changing questions: PASS|FAIL
- Facts separated from assumptions: PASS|FAIL
- Product alternatives and switch conditions: PASS|FAIL
- Security, reliability, observability, and cost covered: PASS|FAIL
- Official evidence and retrieval dates: PASS|FAIL
- Production-readiness claim appropriately bounded: PASS|FAIL
```

- [ ] **Step 4: Commit baseline evidence**

```bash
git add tests/scenarios tests/baselines
git commit -m "test: capture architecture skill baselines"
```

---

### Task 2: Scaffold the portable Plugin and Skill

**Files:**
- Create: `volcengine-architecture/.codex-plugin/plugin.json`
- Create: `volcengine-architecture/skills/design-volcengine-architecture/SKILL.md`
- Create: `volcengine-architecture/skills/design-volcengine-architecture/agents/openai.yaml`
- Create: `volcengine-architecture/skills/design-volcengine-architecture/references/`
- Create: `volcengine-architecture/skills/design-volcengine-architecture/scripts/`

**Interfaces:**
- Consumes: plugin-creator and skill-creator scaffold scripts.
- Produces: valid Plugin and Skill roots.

- [ ] **Step 1: Run the Plugin scaffold**

```bash
python3 /Users/juice/.codex/skills/.system/plugin-creator/scripts/create_basic_plugin.py \
  volcengine-architecture \
  --path "/Users/juice/Desktop/vibe coding/volcengine Architecture" \
  --with-skills
```

- [ ] **Step 2: Run the Skill initializer**

```bash
python3 /Users/juice/.codex/skills/.system/skill-creator/scripts/init_skill.py \
  design-volcengine-architecture \
  --path "/Users/juice/Desktop/vibe coding/volcengine Architecture/volcengine-architecture/skills" \
  --resources scripts,references \
  --interface 'display_name=Volcengine Architecture Designer' \
  --interface 'short_description=Design evidence-backed Volcengine architectures' \
  --interface 'default_prompt=Use $design-volcengine-architecture to turn my business requirements into a Volcengine architecture.'
```

- [ ] **Step 3: Validate untouched scaffolds**

```bash
python3 /Users/juice/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py volcengine-architecture
python3 /Users/juice/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  volcengine-architecture/skills/design-volcengine-architecture
```

Expected: both validators succeed.

- [ ] **Step 4: Commit the scaffold**

```bash
git add volcengine-architecture
git commit -m "chore: scaffold volcengine architecture plugin"
```

---

### Task 3: Define intake, routing, output, and subagent contracts

**Files:**
- Create: `volcengine-architecture/skills/design-volcengine-architecture/references/intake-contract.md`
- Create: `volcengine-architecture/skills/design-volcengine-architecture/references/routing-matrix.md`
- Create: `volcengine-architecture/skills/design-volcengine-architecture/references/architecture-output.md`
- Create: `volcengine-architecture/skills/design-volcengine-architecture/references/subagent-contracts.md`

**Interfaces:**
- Consumes: approved design sections 5, 6, 7, and 9.
- Produces: `ArchitectureBrief`, routing labels, final output schema, and five role envelopes.

- [ ] **Step 1: Write `ArchitectureBrief` and the question-impact gate**

Define these fields in `intake-contract.md`:

```yaml
business_goal: string | unknown
users_and_channels: [string]
critical_flows: [string]
upstream_downstream: [string]
traffic_and_growth: string | unknown
data_scale_and_freshness: string | unknown
availability_slo: string | unknown
rto_rpo: string | unknown
data_classification: string | unknown
region_and_residency: string | unknown
network_boundary: string | unknown
cost_priority: string | unknown
existing_stack_and_migration: string | unknown
team_operations: string | unknown
domain_metrics: [string]
facts: [string]
assumptions: [string]
open_questions: [string]
```

A question passes only if its answer can change product category, topology, data flow/storage, security/compliance, capacity/cost, or delivery phase. Limit questions to two rounds.

- [ ] **Step 2: Write routing labels and dispatch thresholds**

Define the approved scenario, quality, and constraint labels plus:

```text
one product family and no high-risk label -> main Skill only
two or more independent product families -> parallel domain analysis when subagents exist
REGULATED or HIGH_AVAILABILITY or DISASTER_RECOVERY -> independent security/reliability review
COST_SENSITIVE or material scale supplied -> FinOps review
no subagent capability -> run the same role contracts serially
```

- [ ] **Step 3: Write the twelve-section final output contract**

Define the exact mapping header:

```markdown
| Architecture capability | Recommended Volcengine product | Why it fits | Alternative | Switch condition | Evidence |
```

Score requirements, architecture, security, reliability, cost, and evidence from 0–2. Permit `Production readiness: READY` only when all score 2 with no critical open item.

- [ ] **Step 4: Write role request and response envelopes**

For each role, define:

```yaml
request:
  brief: ArchitectureBrief
  scope: [string]
  known_evidence: [url]
response:
  findings: [string]
  decisions: [string]
  alternatives: [string]
  risks: [string]
  evidence:
    - claim: string
      url: string
      source_level: A | B | C
      retrieved_at: YYYY-MM-DD
  uncertainties: [string]
```

Add role-specific fields and prohibit subagents from composing the final user answer.

- [ ] **Step 5: Scan and commit**

```bash
rg -n 'TB''D|TO''DO|implement lat''er|fill i''n' \
  volcengine-architecture/skills/design-volcengine-architecture/references
git add volcengine-architecture/skills/design-volcengine-architecture/references
git commit -m "docs: define architecture orchestration contracts"
```

Expected: the scan returns no matches before commit.

---

### Task 4: Build the stable Volcengine product-family references

**Files:**
- Create: `volcengine-architecture/skills/design-volcengine-architecture/references/product-catalog.md`
- Create: `volcengine-architecture/skills/design-volcengine-architecture/references/ai-and-agent.md`
- Create: `volcengine-architecture/skills/design-volcengine-architecture/references/compute-cloud-native.md`
- Create: `volcengine-architecture/skills/design-volcengine-architecture/references/data-analytics.md`
- Create: `volcengine-architecture/skills/design-volcengine-architecture/references/database-storage.md`
- Create: `volcengine-architecture/skills/design-volcengine-architecture/references/networking-security.md`
- Create: `volcengine-architecture/skills/design-volcengine-architecture/references/media-edge.md`

**Interfaces:**
- Consumes: official Volcengine pages current on implementation date.
- Produces: stable routing hints and official discovery links, without frozen dynamic specifications.

- [ ] **Step 1: Research the official taxonomy**

For each product record only:

```yaml
product_name: string
official_url: url
stable_capabilities: [string]
use_when: [string]
avoid_or_verify_when: [string]
dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
```

- [ ] **Step 2: Write the catalog index and six domain references**

`product-catalog.md` maps families to references and official indexes. Each domain file contains capability decomposition, architecture-changing questions, product-family mappings, integration patterns, review points, dynamic facts to recheck, and official discovery links. Keep each under 250 lines.

- [ ] **Step 3: Audit links and dynamic claims**

```bash
rg -n 'https?://' volcengine-architecture/skills/design-volcengine-architecture/references
rg -n '¥|元/|99\.9|QPS|TPS|GB|TB|配额|地域可用' \
  volcengine-architecture/skills/design-volcengine-architecture/references
```

Inspect every match. Remove unneeded numeric marketing claims; mark all dynamic facts for runtime verification.

- [ ] **Step 4: Commit product references**

```bash
git add volcengine-architecture/skills/design-volcengine-architecture/references
git commit -m "docs: add volcengine product family references"
```

---

### Task 5: Implement the deliverable validator with TDD

**Files:**
- Create: `tests/test_validate_deliverable.py`
- Create: `volcengine-architecture/skills/design-volcengine-architecture/scripts/validate-deliverable.py`

**Interfaces:**
- Consumes: UTF-8 Markdown text or one Markdown path.
- Produces: `validate_markdown(text: str) -> list[str]`; CLI exits `0` with `VALID` or `1` with errors.

- [ ] **Step 1: Write failing tests**

Use `importlib.util.spec_from_file_location` and include:

```python
def test_valid_complete_deliverable_has_no_errors():
    assert validate_markdown(VALID_MARKDOWN) == []

def test_reports_missing_required_section():
    text = VALID_MARKDOWN.replace("## Risk and validation plan", "## Removed")
    assert "missing section: Risk and validation plan" in validate_markdown(text)

def test_requires_mermaid_or_explicit_diagram_degradation():
    text = VALID_MARKDOWN.replace("```mermaid\ngraph TD\nA-->B\n```", "no diagram")
    assert "missing Mermaid diagram or diagram degradation notice" in validate_markdown(text)

def test_ready_requires_full_scores():
    text = VALID_MARKDOWN.replace("Evidence: 2", "Evidence: 1")
    assert "READY requires all completeness scores to equal 2" in validate_markdown(text)

def test_dynamic_fact_requires_official_url_and_date():
    text = VALID_MARKDOWN + "\nThe SLA is 99.95%.\n"
    assert "dynamic fact lacks nearby official evidence and retrieval date" in validate_markdown(text)
```

`VALID_MARKDOWN` contains all twelve headings, the exact mapping header, Mermaid, `Production readiness: NOT READY`, six scores, one official URL, and `Retrieved: 2026-08-08`.

- [ ] **Step 2: Run tests and verify RED**

```bash
python3 -m unittest tests/test_validate_deliverable.py -v
```

Expected: import/file-not-found failure because the validator does not exist.

- [ ] **Step 3: Write minimal implementation**

```python
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
    mapping_header = (
        "| Architecture capability | Recommended Volcengine product | Why it fits "
        "| Alternative | Switch condition | Evidence |"
    )
    if mapping_header not in text:
        errors.append("missing exact product mapping table header")
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
        if re.search(r"critical open item", text, re.IGNORECASE):
            errors.append("READY is incompatible with a critical open item")
    dynamic = re.compile(
        r"price|价格|SLA|quota|配额|region|地域|QPS|TPS|\d+(?:\.\d+)?%",
        re.IGNORECASE,
    )
    dated = re.compile(r"(?:Retrieved:\s*|查询日期：)\d{4}-\d{2}-\d{2}")
    for paragraph in re.split(r"\n\s*\n", text):
        if dynamic.search(paragraph):
            if "volcengine.com" not in paragraph or not dated.search(paragraph):
                errors.append("dynamic fact lacks nearby official evidence and retrieval date")
                break
    return errors
```

Dynamic detection inspects paragraphs containing `price`, `价格`, `SLA`, `quota`, `配额`, `region`, `地域`, `QPS`, `TPS`, or percentages. Such a paragraph requires both `volcengine.com` and a retrieval/query date.

Add an `argparse` CLI with one positional `markdown_file`; read it as UTF-8, print `VALID` and exit `0` when the list is empty, otherwise print each error and exit `1`.

- [ ] **Step 4: Run tests and CLI**

```bash
python3 -m unittest tests/test_validate_deliverable.py -v
python3 volcengine-architecture/skills/design-volcengine-architecture/scripts/validate-deliverable.py --help
```

Expected: five tests pass; help describes one Markdown file argument.

- [ ] **Step 5: Commit validator**

```bash
git add tests/test_validate_deliverable.py \
  volcengine-architecture/skills/design-volcengine-architecture/scripts/validate-deliverable.py
git commit -m "feat: validate architecture deliverable structure"
```

---

### Task 6: Write the orchestration Skill from measured failures

**Files:**
- Modify: `volcengine-architecture/skills/design-volcengine-architecture/SKILL.md`
- Modify: `volcengine-architecture/skills/design-volcengine-architecture/agents/openai.yaml`

**Interfaces:**
- Consumes: baseline failures and direct references.
- Produces: the user-facing workflow for vague or detailed Volcengine architecture requests.

- [ ] **Step 1: Replace scaffold frontmatter**

```yaml
---
name: design-volcengine-architecture
description: Use when a user needs a solution architecture, product selection, migration design, capacity plan, security review, reliability design, or cost-aware technical proposal based on Volcengine products, including vague business requirements spanning AI, cloud native, data, databases, storage, networking, security, media, or edge workloads.
---
```

- [ ] **Step 2: Write the core workflow**

Keep the body under 500 lines. It must load intake, ask impact-gate questions for at most two rounds, classify routing labels, load only relevant product references, verify dynamic facts, dispatch role contracts when supported, integrate and review, render the output contract, and run the validator for file outputs.

For every Task 1 failure, add the smallest positive required slot or observable conditional. Do not add unrelated advice.

- [ ] **Step 3: Regenerate UI metadata**

```bash
python3 /Users/juice/.codex/skills/.system/skill-creator/scripts/generate_openai_yaml.py \
  volcengine-architecture/skills/design-volcengine-architecture \
  --interface 'display_name=Volcengine Architecture Designer' \
  --interface 'short_description=Design evidence-backed Volcengine architectures' \
  --interface 'default_prompt=Use $design-volcengine-architecture to turn my business requirements into a Volcengine architecture.'
```

- [ ] **Step 4: Validate and commit**

```bash
python3 /Users/juice/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  volcengine-architecture/skills/design-volcengine-architecture
wc -l -w volcengine-architecture/skills/design-volcengine-architecture/SKILL.md
git add volcengine-architecture/skills/design-volcengine-architecture/SKILL.md \
  volcengine-architecture/skills/design-volcengine-architecture/agents/openai.yaml
git commit -m "feat: orchestrate volcengine architecture design"
```

Expected: validation succeeds and the Skill is below 500 lines.

---

### Task 7: Forward-test all six scenarios

**Files:**
- Create: `tests/forward/ai-agent.md`
- Create: `tests/forward/cloud-native.md`
- Create: `tests/forward/realtime-data.md`
- Create: `tests/forward/media.md`
- Create: `tests/forward/intelligent-service.md`
- Create: `tests/forward/regulated-finance.md`
- Modify if measured failures require it: `volcengine-architecture/skills/design-volcengine-architecture/SKILL.md`
- Modify if measured failures require it: relevant `references/*.md`

**Interfaces:**
- Consumes: frozen scenarios and completed Skill.
- Produces: uncontaminated responses, seven-check scores, and evidence-driven revisions.

- [ ] **Step 1: Dispatch fresh agents with the Skill**

Use the fixed prefix below followed by the complete literal prompt under the matching heading in `tests/scenarios/architecture-scenarios.md`:

```text
Use $design-volcengine-architecture at
/Users/juice/Desktop/vibe coding/volcengine Architecture/volcengine-architecture/skills/design-volcengine-architecture
to solve the request below. Follow the Skill exactly. Do not inspect tests/baselines or other agents' outputs.

```

Save raw responses under `tests/forward/<scenario>.md`.

- [ ] **Step 2: Score the seven checks and validate completed proposals**

Append the Task 1 checklist as `## Forward observations`. If the correct first response is an interview, continue once with explicit assumptions before validating the completed proposal.

```bash
for file in tests/forward/*.md; do
  python3 volcengine-architecture/skills/design-volcengine-architecture/scripts/validate-deliverable.py "$file"
done
```

- [ ] **Step 3: Repair only measured gaps and rerun affected cases**

Change the smallest positive recipe, field, conditional, or reference. Repeat until at least five scenarios identify critical gaps, all high-risk cases trigger independent review, and no unsupported dynamic fact remains.

- [ ] **Step 4: Commit forward evidence**

```bash
git add tests/forward volcengine-architecture
git commit -m "test: verify volcengine architecture skill scenarios"
```

---

### Task 8: Final verification and portable handoff

**Files:**
- Verify: `volcengine-architecture/.codex-plugin/plugin.json`
- Verify: `volcengine-architecture/skills/design-volcengine-architecture/`
- Verify: `tests/`

**Interfaces:**
- Consumes: all artifacts and test evidence.
- Produces: validated distributable directory and verification report.

- [ ] **Step 1: Run automated tests**

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

- [ ] **Step 2: Validate Skill and Plugin**

```bash
python3 /Users/juice/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  volcengine-architecture/skills/design-volcengine-architecture
python3 /Users/juice/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  volcengine-architecture
```

- [ ] **Step 3: Scan for placeholders and secrets**

```bash
rg -n 'TB''D|TO''DO|\[TO''DO|AKIA|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY' volcengine-architecture tests
find volcengine-architecture -type f -print | sort
```

Expected: no placeholder or credential matches; file list matches the approved design plus generated metadata.

- [ ] **Step 4: Inspect Git state**

```bash
git status --short
git log --oneline --decorate -8
```

Expected: no uncommitted implementation files.

- [ ] **Step 5: Report handoff**

Provide an absolute link to `volcengine-architecture/`, an invocation example, exact tests run, forward-scenario pass count, remaining official-documentation uncertainty, and confirmation that no live Volcengine resources changed.
