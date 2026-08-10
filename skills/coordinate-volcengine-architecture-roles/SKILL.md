---
name: coordinate-volcengine-architecture-roles
description: Coordinate structured requirements, product research, domain architecture, security-reliability, and FinOps review roles for a Volcengine architecture. Use when multiple independent analysis roles must return compatible evidence and decisions.
---

# Subagent Contracts

## Standalone invocation

When invoked directly, choose only the roles justified by the supplied routing labels, execute them in parallel when independent and available or serially otherwise, and return their structured findings in the shared envelope below. Reconcile disagreements explicitly, but do not replace the main architecture skill as owner of the final report.

All roles consume and return platform-neutral structured analysis. The main Skill alone reconciles results and composes the final user answer. Subagents must not compose the final user answer, make unsupported product claims, or silently convert uncertainties into facts.

## Shared envelope

Every role uses this required envelope. `brief` is the `ArchitectureBrief` defined by `$interview-volcengine-requirements`.

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

`known_evidence` contains URLs available before the role begins. Evidence entries state what the URL supports, preserve disagreements, and use `uncertainties` for unanswered or conflicting material.

## requirements-analyst

```yaml
request_additions:
  raw_request: string
  known_context: [string]
response_additions:
  requirement_gaps: [string]
  architecture_changing_questions: [string]
  safe_default_assumptions: [string]
```

Identify facts, requirements gaps, questions that pass the question-impact gate, and safe default assumptions. Do not select specific products or expand the interview beyond architecture-changing questions.

## product-researcher

```yaml
request_additions:
  capabilities_to_verify: [string]
  product_families: [string]
  regions_to_verify: [string]
  dynamic_facts_to_verify: [string]
response_additions:
  verified_capabilities: [string]
  source_types: [string]
  applicability_boundaries: [string]
  conflicting_sources: [string]
```

Prefer official sources. Third-party evidence may discover leads or supplement noncritical practice, but cannot establish product existence, core capability, or an architecture-critical limit.

## domain-architect

```yaml
request_additions:
  routing_labels: [string]
  verified_capabilities: [string]
  domain_boundary: string
response_additions:
  components: [string]
  data_flows: [string]
  candidate_products: [string]
  selection_rationales: [string]
  switch_conditions: [string]
  shared_dependencies: [string]
```

Define domain components, data flows, candidates, alternatives, switch conditions, and risks. Do not assume another domain has solved a shared dependency; report that dependency for main-Skill reconciliation.

## security-reliability-reviewer

```yaml
request_additions:
  candidate_architecture: [string]
  routing_labels: [string]
response_additions:
  identity_and_access_controls: [string]
  network_isolation_controls: [string]
  encryption_and_key_controls: [string]
  audit_and_content_controls: [string]
  single_points_of_failure: [string]
  rto_rpo_gaps: [string]
  disaster_recovery_gaps: [string]
```

Review the integrated candidate independently when `REGULATED`, `HIGH_AVAILABILITY`, or `DISASTER_RECOVERY` is present. Assess identity and access, network isolation, encryption, keys, audit, content safety, single points of failure, RTO/RPO, and recovery gaps.

## finops-reviewer

```yaml
request_additions:
  candidate_architecture: [string]
  usage_assumptions: [string]
response_additions:
  cost_drivers: [string]
  estimation_formulas: [string]
  optimization_levers: [string]
  cost_risks: [string]
  required_usage_data: [string]
```

Analyze cost drivers, formulas, optimization levers, risks, and missing usage data. Do not provide a precise amount when official pricing or needed usage inputs are unavailable.
