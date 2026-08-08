# Routing Matrix

## Labels

A request may carry any number of labels from each group. Labels describe analysis needs, not product selections.

```text
scenario: AI_AGENT, CLOUD_NATIVE, BATCH_DATA, REALTIME_DATA, DATABASE, STORAGE, MEDIA, EDGE
quality: LOW_LATENCY, HIGH_THROUGHPUT, HIGH_AVAILABILITY, DISASTER_RECOVERY
constraint: PRIVATE_NETWORK, DATA_RESIDENCY, REGULATED, COST_SENSITIVE, MIGRATION
```

Derive labels from `ArchitectureBrief` facts and assumptions. Put a label in the rationale only when the relevant field supports it; uncertain labels remain conditional and become an `open_questions` item when they pass the question-impact gate.

## Dispatch rules

| Condition | Required handling |
| --- | --- |
| One product family and no high-risk label | Main Skill only, unless an additive review below is triggered. |
| Two or more independent product families | Parallel domain analysis when subagents exist. |
| `REGULATED`, `HIGH_AVAILABILITY`, or `DISASTER_RECOVERY` | Independent security/reliability review. |
| `COST_SENSITIVE` or material scale supplied | FinOps review. |
| No subagent capability | Run the same role contracts serially. |

Rules are additive: `main_only` means no domain analysis is dispatched, not that it suppresses a mandatory review. The security/reliability and FinOps rules override `main_only` whenever their stated conditions apply; for example, a one-family `COST_SENSITIVE` request runs the main Skill and FinOps review. High-risk labels are `REGULATED`, `HIGH_AVAILABILITY`, and `DISASTER_RECOVERY`. Independent means the reviewer receives the integrated candidate architecture and is not asked to endorse the domain architect's conclusions. A product family is independent only when its analysis can proceed without waiting for another family’s detailed design; shared dependencies are reconciled by the main Skill.

## Routing result

Record the routing result as:

```yaml
routing:
  scenario_labels: [string]
  quality_labels: [string]
  constraint_labels: [string]
  product_families: [string]
  roles: [string]
  execution_mode: parallel | serial | main_only
  rationale: [string]
```

The main Skill resolves cross-domain conflicts, records the trade-off in the final output, and does not let routing labels substitute for evidence.
