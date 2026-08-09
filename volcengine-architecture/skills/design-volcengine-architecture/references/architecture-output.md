# Architecture Output Contract

Produce one Markdown proposal whose first visible content is exactly `## Requirements gap check`, followed by the twelve proposal `##` sections below in order. Leading blank lines and HTML comments are ignored by the validator; no title, summary, question, or other visible content may appear before `## Requirements gap check`. Use conditional wording where `ArchitectureBrief.open_questions` or `ArchitectureBrief.assumptions` affects a decision.

## Required sections

1. `## Executive summary` — recommendation, material trade-offs, and applicability boundary.
2. `## Known facts, assumptions, and open items` — facts, assumptions with switch conditions, and unresolved architecture-changing questions.
3. `## Architecture decisions` — decision, rationale, alternative, and reason not selected.
4. `## Logical architecture` — Mermaid logical diagram, or `Diagram degradation:` followed by components and textual flows.
5. `## Deployment topology` — region, availability-zone, network, ingress, and recovery relationships.
6. `## End-to-end data flow` — numbered flows including synchronous or asynchronous behavior, protocol, data type, storage, and failure handling.
7. `## Volcengine product mapping` — the exact mapping table below.
8. `## Non-functional design` — capacity and elasticity, availability, RTO/RPO, security and compliance, observability, performance, and cost.
9. `## Implementation roadmap` — proof of concept, minimum production, and scale phases with acceptance criteria.
10. `## Risk and validation plan` — probability, impact, mitigation, owner, and validation method.
11. `## Official evidence and freshness` — sources, retrieval dates, evidence level, and dynamic facts needing runtime verification.
12. `## Completeness score` — six scores, open-item status, and production-readiness decision.

## Product mapping table

Use this header exactly, including capitalization and column order:

| Architecture capability | Recommended Volcengine product | Why it fits | Alternative | Switch condition | Evidence |
| --- | --- | --- | --- | --- | --- |

Every recommendation requires evidence appropriate to the claim. Dynamic facts require an official source and a retrieved date. If no supported recommendation exists, name the required capability, state the uncertainty, and do not invent a product match.

## Completeness and readiness

Score each dimension from `0` through `2`:

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Requirements | Missing or contradictory | Partly bounded with material open items | Architecture-changing needs are bounded or explicitly conditional |
| Architecture | No coherent end-to-end design | Plausible design with unresolved dependencies | Decisions, topology, and flows are coherent and traceable |
| Security | Not assessed | Controls or gaps partly identified | Controls, boundaries, and residual risks are addressed |
| Reliability | Not assessed | Some failure handling or recovery described | Availability, failure handling, RTO/RPO, and recovery are addressed |
| Cost | Not assessed | Drivers or estimates incomplete | Drivers, assumptions, levers, and cost risks are addressed |
| Evidence | Unsupported claims | Partial or stale support | Architecture-changing claims have suitable, current evidence |

Write scores as separate lines exactly in this form:

```text
Requirements: 0
Architecture: 0
Security: 0
Reliability: 0
Cost: 0
Evidence: 0
Production readiness: NOT READY
```

Write exactly one `Production readiness: READY` or `Production readiness: NOT READY` line. `Production readiness: READY` is permitted only when every one of the six scores equals `2` and there is no critical open item. Otherwise write `Production readiness: NOT READY` and identify the blocking item or condition.
