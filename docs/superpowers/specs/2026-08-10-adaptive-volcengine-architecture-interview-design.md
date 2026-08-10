# Adaptive Volcengine Architecture Interview Design

Date: 2026-08-10
Status: approved in conversation; awaiting written-spec review
Scope: improve `design-volcengine-architecture`

## 1. Goal

Upgrade the existing architecture Skill from a short gap check into an adaptive, one-question-at-a-time interview. The interview must collect only architecture-changing information, allow the user to continue with explicit defaults, and produce a report whose important capabilities map to concrete Volcengine products.

The result should feel conversational like `grill-me`, while remaining bounded and useful for users who already supplied enough detail.

## 2. Non-goals

- Do not provision or modify Volcengine resources.
- Do not turn the Skill into a fixed questionnaire that asks irrelevant questions.
- Do not require the user to know Volcengine product names.
- Do not claim current availability, commercial terms, limits, or service commitments without runtime verification.
- Do not replace architectural reasoning with a product list.
- Do not require multi-agent execution.

## 3. Chosen approach

Use a contract-driven adaptive interview rather than a prompt-only enhancement or a deterministic questionnaire script.

The Skill will maintain an `ArchitectureBrief`, select the single highest-impact unresolved question, update the brief after every answer, and stop when additional answers cannot materially change product choice, topology, data flow, security, capacity, cost, or delivery phase.

This approach preserves natural dialogue while giving the report and validator explicit, testable requirements.

## 4. Interview state machine

```text
requirements gap scan
  -> single-question interview
  -> architecture branch confirmation
  -> report generation
```

### 4.1 Requirements gap scan

The first response summarizes:

- known facts;
- architecture-changing gaps;
- safe assumptions available if the user wants to continue immediately.

It does not recommend products before the architecture-changing gaps are either answered or converted into explicit assumptions.

### 4.2 Single-question interview

Ask exactly one question per assistant turn. Select the highest-impact unresolved topic in this order unless the supplied context makes another topic more consequential:

1. business goal and critical flow;
2. data sensitivity, compliance, and network boundary;
3. traffic, data scale, freshness, and growth;
4. availability objective, RTO, and RPO;
5. existing systems, migration constraints, team skills, and operating model;
6. cost, performance, and delivery-speed priority.

Each question must:

- pass the existing question-impact gate;
- offer a recommended answer when a safe default exists;
- explain which product family, topology, flow, control, or phase changes across the answer branches;
- avoid asking for information already supplied;
- update the brief immediately after the user answers.

### 4.3 User-controlled exit

Stop interviewing when the user says an equivalent of:

- proceed with defaults;
- produce a proposal now;
- unknown or unable to answer.

Convert every unresolved architecture-changing gap into:

```text
Assumption: <condition used by the proposal>.
Switch condition: If <different answer>, change <product, topology, flow, security, cost, or phase decision>.
```

### 4.4 Automatic stop

Stop when no unresolved question can materially change the architecture. Use a hard ceiling of eight single-question turns to prevent an endless interview; the expected path is three to five questions. An information-rich request may skip the interview entirely.

## 5. Concrete product mapping contract

The report must not use generic capability categories as final component names. Important components must map to a concrete Volcengine product, for example:

| Capability | Concrete product examples |
| --- | --- |
| Container orchestration | 容器服务 |
| Elastic compute | 云服务器 ECS, GPU云服务器, 函数服务 |
| Object storage | 对象存储 TOS |
| Relational database | 云数据库 MySQL 版, 云数据库 PostgreSQL 版 |
| Cache | 缓存数据库 Redis 版 |
| Messaging | 消息队列 Kafka版 |
| Stream processing | 流式计算 Flink版 |
| Analytical warehouse | ByteHouse 企业版 |
| Foundation models and inference | 火山方舟 |
| Traffic distribution | 负载均衡, 内容分发网络 CDN |
| Application protection | Web应用防火墙 |
| Logging and monitoring | 日志服务 TLS |
| Identity and access | 访问控制 IAM |
| Network interconnection | 专线连接 |

The domain references remain the authority for canonical display names and official discovery URLs. Product examples in this design do not authorize unverified dynamic claims.

Every material product mapping must include:

- canonical product name and common abbreviation when one exists;
- responsibility in this architecture;
- requirement-linked selection rationale;
- one viable Volcengine alternative or self-managed alternative;
- an observable switch condition;
- an official Volcengine product or documentation URL;
- retrieval date;
- explicit runtime-verification status for dynamic facts.

## 6. Report contract

Continue writing the source-of-truth report to `reports/volcengine-architecture-report.md` unless the caller requests another path.

The report contains:

1. interview conclusion: confirmed facts, user choices, assumptions, and open items;
2. executive summary: recommendation, concrete product set, scope, and trade-offs;
3. architecture decisions with requirement rationale, alternative, rejection reason, and switch condition;
4. Mermaid logical architecture whose important nodes use concrete product names;
5. deployment topology including boundaries, availability-zone relationships, ingress, subnets, and recovery relationships;
6. numbered end-to-end flows with protocol, sync/async behavior, data type, stores, and failure handling;
7. concrete Volcengine product mapping;
8. security, reliability, observability, performance, capacity, and cost design;
9. PoC, minimum-production, and scale phases with acceptance criteria;
10. risks, validation plan, evidence freshness, completeness scores, and bounded readiness.

The existing twelve-section output order remains stable for compatibility. The richer interview conclusion is represented inside the requirements-gap and known-facts sections rather than introducing incompatible top-level headings.

## 7. Consistency and validation

Extend the deliverable validator so it rejects reports when:

- the product mapping contains no recognizable concrete Volcengine product;
- a critical architecture-diagram product is absent from the mapping table;
- a recommendation lacks a responsibility, alternative, or switch condition;
- a product capability claim lacks an official Volcengine URL and retrieval date;
- generic terms such as database, cache, object storage, or message queue remain unexplained placeholders instead of capability labels paired with concrete products;
- the interview ended with unresolved architecture-changing gaps but the report records neither assumptions nor switch conditions.

Generic terms remain valid in explanatory prose and capability-column labels. Validation targets unresolved component placeholders, not ordinary language.

Keep product-name recognition data in one reusable reference or validator data structure so the product catalog, output rules, and validator do not drift independently.

## 8. Failure handling

- If the user cannot answer, adopt a stated default and preserve the branch that would change the design.
- If no concrete product can be verified, state the required capability and mark product selection as unresolved; do not invent a name.
- If official product naming differs across current pages, use the most specific verified name and preserve the naming conflict as an open item.
- If network access is unavailable, use known catalog entries only as discovery candidates and mark product availability and dynamic facts for runtime verification.
- If the validator finds inconsistent diagram, flow, and product mapping names, fix the report before delivery.

## 9. Test strategy

Apply skill TDD to the behavioral change.

### 9.1 Baseline tests

Run fresh-context scenarios against the pre-change Skill and record whether it:

- asks more than one question in a turn;
- stops after the old two-round limit despite consequential gaps;
- generates a complete proposal too early;
- uses generic component categories instead of concrete Volcengine products;
- produces a product mapping that is inconsistent with the diagram or flows.

### 9.2 Forward tests

Run the same scenarios against the revised Skill:

1. A vague workload must enter one-question-at-a-time interviewing and must not emit a completed proposal immediately.
2. A user asking to proceed immediately must receive explicit assumptions and switch conditions before the report.
3. An information-rich workload must minimize or skip questions while still producing a concrete product architecture.
4. A cross-domain workload must map every critical component to a named Volcengine product and keep diagram, flow, and mapping names consistent.
5. An unverifiable product or dynamic fact must remain unresolved rather than being invented.

### 9.3 Automated tests

Add validator tests for:

- at least one concrete-product mapping;
- generic-only mappings failing;
- missing responsibility, alternative, or switch condition failing;
- critical diagram products missing from the mapping failing;
- assumptions and switch conditions required after an incomplete interview;
- a complete, evidence-backed report continuing to pass.

## 10. Files expected to change

- `SKILL.md`: replace the two-round interview rule with the adaptive state machine and user exit.
- `references/intake-contract.md`: add interview state, question ranking, stopping criteria, and answer normalization.
- `references/product-catalog.md` and selected domain references: normalize canonical product names and stable aliases needed for concrete mapping.
- `references/architecture-output.md`: strengthen concrete product and cross-section consistency requirements.
- `references/report-contract.md`: include the interview conclusion and concrete-product obligations.
- `scripts/validate-deliverable.py`: add concrete-product, row-completeness, consistency, and assumption checks.
- repository tests and scenario artifacts: capture RED and GREEN behavior.
- `agents/openai.yaml`: update only if its prompt or description no longer reflects the Skill.

## 11. Acceptance criteria

- The Skill asks one architecture-changing question per turn.
- It supports explicit early continuation with defaults.
- It stops automatically when further answers cannot change the architecture and never exceeds eight interview turns.
- Information-rich prompts do not receive unnecessary questions.
- Every critical architecture component is either mapped to a concrete verified Volcengine product or explicitly marked unresolved.
- Product mappings contain responsibility, rationale, alternative, switch condition, official URL, and retrieval date.
- Diagram, flows, decisions, and mapping use consistent product names.
- The final report passes the extended validator.
- Baseline and forward-test evidence demonstrates the intended behavioral change.
