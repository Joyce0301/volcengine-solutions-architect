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

## Question-impact gate

Ask a question only when materially different answers can change at least one of these decisions:

- product category;
- topology;
- data flow or storage;
- security or compliance;
- capacity or cost; or
- delivery phase.

Reject questions that only add background, confirm a decision already fixed by the request, or do not change one of the listed decisions. Ask at most two rounds. When an answer remains unavailable after the second round, record an explicit assumption and its switch condition in `assumptions`, retain the gap in `open_questions`, and use a conditional design rather than inventing a fact.

## Intake handoff

The completed `ArchitectureBrief` is the only requirements payload passed to routing and role contracts. Preserve its exact field names; role-specific data belongs in that role's request envelope.
