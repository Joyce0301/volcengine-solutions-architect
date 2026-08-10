---
name: write-volcengine-architecture-report
description: Write and quality-gate the final Volcengine architecture report. Use when persisting a completed architecture, validating its Markdown contract, and returning the report path with decisions and open items.
---

# Final Architecture Report Contract

## Standalone invocation

When invoked directly, accept a completed architecture candidate, write it to the requested path or the default path below, run the shared validator, and fix structural failures before returning. Return the absolute report path plus a concise summary of decisions, assumptions, and blocking open items. Do not perform product research or invent missing architecture decisions in this persistence step.

A completed architecture is not complete until the final result and its supporting details are written to a self-contained Markdown report. The report is the source of truth for handoff, review, implementation, and later updates; the chat response is only a concise summary.

## Report location

- Default path: `reports/volcengine-architecture-report.md`, relative to the caller's working directory.
- If the caller provides a report path, use that path instead and create parent directories as needed.
- Even for chat-only requests, create the local report and return its absolute path.
- Do not create the final report during the interview. Create it only after architecture-changing question rounds are complete and assumptions or switch conditions are recorded.

## Required report content

The report must contain the exact twelve-section architecture output contract from `$render-volcengine-architecture`, plus enough detail for another architect to reproduce the decisions. Include:

- requirements gaps, known facts, user answers, assumptions, switch conditions, and unresolved items;
- executive recommendation, scope boundary, and material trade-offs;
- routing labels, role passes, and the rationale for the selected execution mode;
- every material architecture decision, rationale, considered alternative, rejection reason, and switch condition;
- a logical architecture diagram or an explicit diagram-degradation explanation;
- deployment topology, deployment location, availability-zone relationships, VPC/subnets, ingress, and disaster recovery;
- numbered synchronous/asynchronous flows with protocol, data type, stores, and failure handling;
- concrete Volcengine product mappings with responsibilities, alternatives, switch conditions, official evidence, and retrieval dates;
- security, compliance, reliability, observability, performance, capacity, cost drivers, and unresolved commercial/runtime facts;
- PoC, minimum-production, and scale phases with measurable acceptance criteria;
- risks with probability, impact, mitigation, owner, and validation method;
- evidence freshness, completeness scores, dynamic-fact verification status, and bounded production readiness.

Keep facts, assumptions, and open items visibly separate. Summarize the resulting interview state and decisions; do not substitute a verbatim interview transcript or a list of products for the final architecture result. Keep canonical product names consistent across decisions, diagram, flows, and the mapping table.

## Quality gate

Run `../design-volcengine-architecture/scripts/validate-deliverable.py` against the report path and fix all structural errors before returning it. Return the absolute report path and summarize the final decisions, key assumptions, and blocking open items. A passing validator confirms the report contract is present; it does not replace technical review.
