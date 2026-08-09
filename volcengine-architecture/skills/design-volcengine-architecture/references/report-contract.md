# Final Architecture Report Contract

A completed architecture is not complete until the final result and its supporting details are written to a self-contained Markdown report. The report is the source of truth for handoff, review, implementation, and later updates; the chat response is only a concise summary.

## Report location

- Default path: `reports/volcengine-architecture-report.md`, relative to the caller's working directory.
- If the caller provides a report path, use that path instead and create parent directories as needed.
- Even for chat-only requests, create the local report and return its absolute path.
- Do not create the final report during the interview. Create it only after architecture-changing question rounds are complete and assumptions or switch conditions are recorded.

## Required report content

The report must contain the exact twelve-section architecture output contract from `architecture-output.md`, plus enough detail for another architect to reproduce the decisions. Include:

- requirements gaps, known facts, assumptions, and unresolved items;
- executive recommendation, scope boundary, and material trade-offs;
- routing labels, role passes, and the rationale for the selected execution mode;
- every material architecture decision, rationale, considered alternative, rejection reason, and switch condition;
- a logical architecture diagram or an explicit diagram-degradation explanation;
- deployment topology, deployment location, availability-zone relationships, VPC/subnets, ingress, and disaster recovery;
- numbered synchronous/asynchronous flows with protocol, data type, stores, and failure handling;
- concrete Volcengine product mappings, alternatives, switch conditions, official evidence, and retrieval dates;
- security, compliance, reliability, observability, performance, capacity, cost drivers, and unresolved commercial/runtime facts;
- PoC, minimum-production, and scale phases with measurable acceptance criteria;
- risks with probability, impact, mitigation, owner, and validation method;
- evidence freshness, completeness scores, dynamic-fact verification status, and bounded production readiness.

Keep facts, assumptions, and open items visibly separate. Do not substitute an interview transcript or a list of products for the final architecture result.

## Quality gate

Run `scripts/validate-deliverable.py` against the report path and fix all structural errors before returning it. Return the absolute report path and summarize the final decisions, key assumptions, and blocking open items. A passing validator confirms the report contract is present; it does not replace technical review.
