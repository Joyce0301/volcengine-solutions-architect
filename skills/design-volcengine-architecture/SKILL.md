---
name: design-volcengine-architecture
description: Use when a user needs a solution architecture, product selection, migration design, capacity plan, security review, reliability design, or cost-aware technical proposal based on Volcengine products, including vague business requirements spanning AI, cloud native, data, databases, storage, networking, security, media, or edge workloads.
---

# Design Volcengine Architecture

Design Volcengine architectures from business requirements. Start with gaps, separate facts from assumptions, use official evidence for product claims, and keep production readiness bounded by the evidence and open items.

## Core Workflow

1. Use `$interview-volcengine-requirements` before asking or designing. Normalize the request into `ArchitectureBrief` fields.
2. The first visible content in any architecture response must be this exact requirements gap block, before executive summary, questions, routing, products, topology, or recommendations:
   - `## Requirements gap check`
   - `Known facts`
   - `Architecture-changing gaps`
   - `Assumptions if unanswered`
   If the first response is an interview, still start with this block and then ask only gated questions. If proceeding to a full proposal, keep this block as a required preface, then render the exact twelve-section proposal below.
3. Run the adaptive interview defined by `$interview-volcengine-requirements`. Ask exactly one question per assistant turn, selecting the unresolved question with the highest architectural impact. Stop when no remaining answer can change the architecture, the user asks to proceed with defaults, or the interview reaches a hard ceiling of eight questions. Convert unresolved gaps into explicit assumptions and switch conditions.
4. Use `$route-volcengine-architecture`. Assign scenario, quality, and constraint labels with a one-line rationale for each label. In any full proposal, write the fenced `routing:` record before `## Architecture decisions`; do not make product or topology decisions before this record is visible.
5. Use `$select-volcengine-products`, then invoke only the independently callable domain skills selected by routing:
   - `AI_AGENT` -> `$design-volcengine-ai-agent`
   - `CLOUD_NATIVE` -> `$design-volcengine-cloud-native`
   - `BATCH_DATA` or `REALTIME_DATA` -> `$design-volcengine-data-analytics`
   - `DATABASE` or `STORAGE` -> `$design-volcengine-database-storage`
   - `PRIVATE_NETWORK`, `DATA_RESIDENCY`, `REGULATED`, or public ingress/security review -> `$design-volcengine-network-security`
   - `MEDIA` or `EDGE` -> `$design-volcengine-media-edge`
6. Verify dynamic facts at runtime before relying on them: price, region, specification, quota, SLA, version status, promotion, exact limits, or current model/product availability. If you assert a dynamic fact, the same paragraph or table cell must include an official `volcengine.com` URL and `Retrieved: YYYY-MM-DD` or `查询日期：YYYY-MM-DD`. If network access is unavailable or you choose not to verify, do not assert the dynamic value; state the field is `unknown` or `requires runtime verification` and keep it in open items without naming concrete prices, regions, quotas, SLAs, percentages, QPS/TPS values, exact limits, model availability, or specification values. Use validator-safe synonyms for unverified topology and commercial facts: `deployment location`, `commercial terms`, `capacity target`, `service target`, and `runtime verification required`. Write `secure HTTP` instead of `HTTPS` unless the same paragraph includes official evidence and retrieval date.
7. If routing calls for role work, use `$coordinate-volcengine-architecture-roles`, then choose execution mode. Dispatch the relevant contracts when subagents are available; otherwise run the same contracts serially in the main context. The main Skill owns conflict resolution and the final answer.
8. Integrate domain findings into one architecture. Map every material capability to a concrete Volcengine product when official evidence supports the match. Include its responsibility, rationale, alternative, and switch condition; otherwise keep the capability unresolved instead of inventing a product.
9. Review the candidate explicitly for security, reliability, observability, and cost. When `REGULATED`, `HIGH_AVAILABILITY`, or `DISASTER_RECOVERY` is present, include an independent security/reliability review result. When `COST_SENSITIVE` or material scale is supplied, include FinOps findings.
10. Use `$render-volcengine-architecture` to render the exact twelve-section proposal with the required field details and scoring rules.
11. Use `$write-volcengine-architecture-report`. When the adaptive interview is complete or has exited with explicit assumptions, write the final architecture result and all supporting details to `reports/volcengine-architecture-report.md` (or the caller-requested report path). The report is the source of truth; do not return a completed architecture only in chat without creating the report.
12. For the report Markdown deliverable, run:

```text
python3 "<SKILL_ROOT>/scripts/validate-deliverable.py" <markdown_file>
```

13. Resolve `<SKILL_ROOT>` at runtime to the absolute directory containing this `SKILL.md`, using the host platform's native path handling; do not assume the process is running from the repository or plugin directory. Fix structural validator errors before returning the report. Passing the validator does not prove the architecture is correct; it proves required evidence and output slots are present. Return the absolute report path and summarize final decisions.

## Question Rules

Ask a question only when a different answer can change product category, topology, data flow or storage, security/compliance, capacity/cost, or delivery phase. Ask exactly one question per assistant turn. State the recommended answer when a safe default exists and briefly name the decision that different answers would change.

Do not ask questions that merely make the brief more complete or repeat supplied facts. After each answer, update `ArchitectureBrief` and select the next highest-impact gap. End automatically when no unresolved question can materially change the architecture. If the user says `proceed with defaults`, asks for a proposal now, cannot answer, or the interview reaches the hard ceiling of eight questions, continue with assumptions in this form:

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
- Product mapping rows with a concrete product name, responsibility, requirement-linked rationale, alternative, switch condition, and official evidence. Generic labels such as database, cache, object storage, or message queue may identify a capability but may not replace the product name.
- Consistent concrete product names across architecture decisions, Mermaid nodes, end-to-end flows, and the product mapping table.
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
| Architecture capability | Recommended Volcengine product | Responsibility | Why it fits | Alternative | Switch condition | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
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
| Questions are broad, bundled, or endless | Ask one highest-impact question per turn and stop adaptively, with a hard ceiling of eight. |
| Products remain generic capability labels | Use the canonical concrete product name from the routed domain reference or mark the match unresolved. |
| Facts and assumptions blur | Maintain separate facts, assumptions, open items, and evidence. |
| Products are single-path | Add alternatives and switch conditions to each material choice. |
| Security, reliability, observability, or cost is thin | Add explicit coverage in `Non-functional design` and risk review. |
| Current facts lack evidence | Cite official URLs with retrieval dates or mark unverified. |
| Readiness is overclaimed | Score completeness and mark `NOT READY` unless all readiness conditions pass. |
