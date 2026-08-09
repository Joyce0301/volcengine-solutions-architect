---
name: design-volcengine-architecture
description: Use when a user needs a solution architecture, product selection, migration design, capacity plan, security review, reliability design, or cost-aware technical proposal based on Volcengine products, including vague business requirements spanning AI, cloud native, data, databases, storage, networking, security, media, or edge workloads.
---

# Design Volcengine Architecture

Design Volcengine architectures from business requirements. Start with gaps, separate facts from assumptions, use official evidence for product claims, and keep production readiness bounded by the evidence and open items.

## Core Workflow

1. Read [references/intake-contract.md](references/intake-contract.md) before asking or designing. Normalize the request into `ArchitectureBrief` fields.
2. The first visible content in any architecture response must be this exact requirements gap block, before executive summary, questions, routing, products, topology, or recommendations:
   - `## Requirements gap check`
   - `Known facts`
   - `Architecture-changing gaps`
   - `Assumptions if unanswered`
   If the first response is an interview, still start with this block and then ask only gated questions. If proceeding to a full proposal, keep this block as a required preface, then render the exact twelve-section proposal below.
3. Ask only questions that pass the question-impact gate from `intake-contract.md`. Ask at most two rounds. If the user cannot answer or the second round is complete, proceed with explicit assumptions and switch conditions.
4. Read [references/routing-matrix.md](references/routing-matrix.md). Assign scenario, quality, and constraint labels with a one-line rationale for each label. In any full proposal, write the fenced `routing:` record before `## Architecture decisions`; do not make product or topology decisions before this record is visible.
5. Load [references/product-catalog.md](references/product-catalog.md), then load only the domain references selected by routing:
   - `AI_AGENT` -> [references/ai-and-agent.md](references/ai-and-agent.md)
   - `CLOUD_NATIVE` -> [references/compute-cloud-native.md](references/compute-cloud-native.md)
   - `BATCH_DATA` or `REALTIME_DATA` -> [references/data-analytics.md](references/data-analytics.md)
   - `DATABASE` or `STORAGE` -> [references/database-storage.md](references/database-storage.md)
   - `PRIVATE_NETWORK`, `DATA_RESIDENCY`, `REGULATED`, or public ingress/security review -> [references/networking-security.md](references/networking-security.md)
   - `MEDIA` or `EDGE` -> [references/media-edge.md](references/media-edge.md)
6. Verify dynamic facts at runtime before relying on them: price, region, specification, quota, SLA, version status, promotion, exact limits, or current model/product availability. If you assert a dynamic fact, the same paragraph or table cell must include an official `volcengine.com` URL and `Retrieved: YYYY-MM-DD` or `查询日期：YYYY-MM-DD`. If network access is unavailable or you choose not to verify, do not assert the dynamic value; state the field is `unknown` or `requires runtime verification` and keep it in open items without naming concrete prices, regions, quotas, SLAs, percentages, QPS/TPS values, exact limits, model availability, or specification values. Use validator-safe synonyms for unverified topology and commercial facts: `deployment location`, `commercial terms`, `capacity target`, `service target`, and `runtime verification required`. Write `secure HTTP` instead of `HTTPS` unless the same paragraph includes official evidence and retrieval date.
7. If the routing matrix calls for role work, read [references/subagent-contracts.md](references/subagent-contracts.md), then choose execution mode. Dispatch the relevant contracts when subagents are available; otherwise run the same contracts serially in the main context. The main Skill owns conflict resolution and the final answer.
8. Integrate domain findings into one architecture. Include alternatives and switch conditions for every material product recommendation or topology choice.
9. Review the candidate explicitly for security, reliability, observability, and cost. When `REGULATED`, `HIGH_AVAILABILITY`, or `DISASTER_RECOVERY` is present, include an independent security/reliability review result. When `COST_SENSITIVE` or material scale is supplied, include FinOps findings.
10. Render the final proposal using the exact twelve-section output below. Read [references/architecture-output.md](references/architecture-output.md) for field details and scoring rules.
11. Read [references/report-contract.md](references/report-contract.md). When architecture-changing question rounds are complete, write the final architecture result and all supporting details to `reports/volcengine-architecture-report.md` (or the caller-requested report path). The report is the source of truth; do not return a completed architecture only in chat without creating the report.
12. For the report Markdown deliverable, run:

```text
python3 "<SKILL_ROOT>/scripts/validate-deliverable.py" <markdown_file>
```

13. Resolve `<SKILL_ROOT>` at runtime to the absolute directory containing this `SKILL.md`, using the host platform's native path handling; do not assume the process is running from the repository or plugin directory. Fix structural validator errors before returning the report. Passing the validator does not prove the architecture is correct; it proves required evidence and output slots are present. Return the absolute report path and summarize final decisions.

## Question Rules

Ask a question only when a different answer can change product category, topology, data flow or storage, security/compliance, capacity/cost, or delivery phase.

Do not ask questions that merely make the brief more complete. After two rounds, continue with assumptions in this form:

```text
Assumption: <assumed condition>.
Switch condition: If <different answer>, change <product/topology/flow/security/cost/phase decision>.
```

## Evidence Rules

- A-level evidence: official Volcengine product docs, product pages, price pages, SLA pages, trust, security, and compliance materials.
- B-level evidence: official Volcengine cases, whitepapers, and repositories.
- C-level evidence: third-party material. Use only as a lead or noncritical practice support.
- Product existence, core capability, architecture-critical limits, SLA, compliance, price, region, specification, quota, and version status require A-level evidence.
- For unverified dynamic/current items, use validator-safe wording such as `Runtime verification required for product availability and commercial terms.` Avoid trigger words, including the literal words `region`, `地域`, `price`, `价格`, `SLA`, `quota`, `配额`, `QPS`, `TPS`, `HTTPS`, percentages, and exact limits, unless the same paragraph has official Volcengine evidence and a retrieval date.
- If official sources conflict, prefer the more specific and more recently updated source. If priority is unclear, preserve the conflict as an open item.
- Never invent exact costs, SLA, regions, quotas, model limits, or specifications from memory.

## Routing And Role Labels

Record routing in the final design notes before architecture decisions:

```yaml
routing:
  scenario_labels: [AI_AGENT | CLOUD_NATIVE | BATCH_DATA | REALTIME_DATA | DATABASE | STORAGE | MEDIA | EDGE]
  quality_labels: [LOW_LATENCY | HIGH_THROUGHPUT | HIGH_AVAILABILITY | DISASTER_RECOVERY]
  constraint_labels: [PRIVATE_NETWORK | DATA_RESIDENCY | REGULATED | COST_SENSITIVE | MIGRATION]
  product_families: [string]
  roles: [requirements-analyst | product-researcher | domain-architect | security-reliability-reviewer | finops-reviewer]
  execution_mode: parallel | serial | main_only
  rationale: [string]
```

Use roles as optional execution structure, not as a dependency. If multi-agent execution is unavailable, perform each required role serially and label the output `serial role pass`.

## Design Requirements

Every final proposal must contain:

- A facts, assumptions, and open-items split.
- A fenced `routing:` record before `## Architecture decisions`.
- Architecture decisions with rationale, alternative, and reason not selected.
- Mermaid logical architecture or an explicit `Diagram degradation:` notice.
- Deployment topology covering deployment location or unresolved deployment location, availability zones, VPC, subnets, ingress, and disaster recovery relationships. Use the literal word `region` only with official evidence and retrieval date in the same paragraph.
- Numbered end-to-end flows with sync/async behavior, protocol, data type, storage, and failure handling.
- Product mapping rows with alternative and switch condition.
- Security, reliability, observability, performance, and cost coverage.
- PoC, minimum production, and scale phases with acceptance criteria.
- Risks with probability, impact, mitigation, owner, and validation method.
- Official evidence with retrieval dates for every dynamic or architecture-critical claim.
- Six completeness scores and a bounded readiness decision.

## Exact Final Output

Start final responses with `## Requirements gap check`, then use these twelve section headings in this order. After `## Known facts, assumptions, and open items` and before `## Architecture decisions`, insert the required fenced `routing:` record.

````markdown
## Executive summary
## Known facts, assumptions, and open items
```yaml
routing:
  scenario_labels: [string]
  quality_labels: [string]
  constraint_labels: [string]
  product_families: [string]
  roles: [string]
  execution_mode: serial
  rationale: [string]
```
## Architecture decisions
## Logical architecture
## Deployment topology
## End-to-end data flow
## Volcengine product mapping
## Non-functional design
## Implementation roadmap
## Risk and validation plan
## Official evidence and freshness
## Completeness score
````

Use this product mapping header exactly:

```markdown
| Architecture capability | Recommended Volcengine product | Why it fits | Alternative | Switch condition | Evidence |
| --- | --- | --- | --- | --- | --- |
```

Every product mapping `Evidence` cell must include an official `volcengine.com` URL and `Retrieved: YYYY-MM-DD`, even when the URL is only a discovery entry and runtime verification is still required.

End with these score lines, using values `0`, `1`, or `2`:

```text
Requirements: 0
Architecture: 0
Security: 0
Reliability: 0
Cost: 0
Evidence: 0
Production readiness: NOT READY
```

`Production readiness: READY` is allowed only when all six scores are `2` and there is no critical open item. Otherwise write `Production readiness: NOT READY` and state the blocker.

## Production Readiness Boundary

The first response may be an interview when architecture-changing facts are missing. A completed proposal is bounded production guidance, not a deployment authorization. Do not claim implementation-ready or production-ready status when any critical requirement, official evidence, security control, RTO/RPO, cost driver, or operational owner remains unresolved.

## Common Failure Corrections

| Baseline failure | Required correction |
| --- | --- |
| Solution starts before gaps | Start with known facts, architecture-changing gaps, and assumptions. |
| Questions are broad or endless | Ask only question-impact-gate questions and stop after two rounds. |
| Facts and assumptions blur | Maintain separate facts, assumptions, open items, and evidence. |
| Products are single-path | Add alternatives and switch conditions to each material choice. |
| Security, reliability, observability, or cost is thin | Add explicit coverage in `Non-functional design` and risk review. |
| Current facts lack evidence | Cite official URLs with retrieval dates or mark unverified. |
| Readiness is overclaimed | Score completeness and mark `NOT READY` unless all readiness conditions pass. |
