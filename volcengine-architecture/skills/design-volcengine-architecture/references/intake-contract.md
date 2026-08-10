# Intake Contract

## ArchitectureBrief

Normalize the request into this platform-neutral record before researching or designing. `unknown` means the information is not available; it is not a claim about the target architecture.

```yaml
ArchitectureBrief:
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

Populate every list with zero or more items. Keep supplied facts separate from assumptions and unanswered questions. An assumption must state the architecture branch that changes if it proves false.

## Adaptive interview state

Track this state in the conversation; do not pass it to domain roles as a requirement fact:

```yaml
InterviewState:
  status: gap_scan | interviewing | branch_confirmation | report
  questions_asked: integer
  answered_fields: [ArchitectureBrief field]
  candidate_questions: [string]
  exit_reason: sufficient | proceed_with_defaults | user_unknown | ceiling
```

Move from `gap_scan` to `interviewing` only when an unresolved answer can change an architectural decision. Move to `branch_confirmation` when the user exits early and assumptions must be recorded. Move directly to `report` when the request is already sufficient or no unresolved question can materially change the architecture.

## Question-impact gate

Ask a question only when materially different answers can change at least one of these decisions:

- product category;
- topology;
- data flow or storage;
- security or compliance;
- capacity or cost; or
- delivery phase.

Reject questions that only add background, confirm a decision already fixed by the request, or do not change one of the listed decisions. Ask exactly one question per assistant turn and immediately normalize the answer into `ArchitectureBrief` before choosing another question.

Rank unresolved topics by expected architectural impact:

1. business goal and critical flow;
2. data sensitivity, compliance, and network boundary;
3. traffic, data scale, freshness, and growth;
4. availability objective, RTO, and RPO;
5. existing systems, migration constraints, team skills, and operating model;
6. cost, performance, and delivery-speed priority.

For each question, provide a recommended option when a safe default exists and identify the product family, topology, flow, control, capacity model, or phase that changes across answer branches. Do not repeat answered questions.

Stop when no unresolved question can materially change product choice, topology, data flow or storage, security or compliance, capacity or cost, or delivery phase. Also stop when the user asks to `proceed with defaults`, requests a proposal now, cannot answer, or the interview reaches a hard ceiling of eight questions.

For every unresolved architecture-changing gap, record both lines:

```text
Assumption: <condition used by the proposal>.
Switch condition: If <different answer>, change <product, topology, flow, security, cost, or phase decision>.
```

Retain the gap in `open_questions` and use a conditional design rather than inventing a fact. An information-rich request may skip interviewing.

## Intake handoff

The completed `ArchitectureBrief` is the only requirements payload passed to routing and role contracts. Preserve its exact field names; role-specific data belongs in that role's request envelope.
