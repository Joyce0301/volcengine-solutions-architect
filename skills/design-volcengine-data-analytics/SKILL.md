---
name: design-volcengine-data-analytics
description: Design Volcengine batch, streaming, lakehouse, warehouse, and data-governance architectures. Use for ingestion, Kafka, Flink, DataLeap, LAS, ByteHouse, replay, and analytical serving decisions.
---

# Data and Analytics

## Standalone invocation

When invoked directly, design only the requested data and analytics domain boundary. Separate known facts, assumptions, and architecture-changing gaps; then map each material capability to a canonical product from this skill. For every recommendation include responsibility, rationale, alternative, switch condition, and official discovery URL. Add a retrieval date only after opening that official page during the current task; otherwise mark runtime verification required. Keep unverified dynamic facts unresolved and identify shared storage, compute, network, security, or serving dependencies for other skills.

## Capability decomposition

- Separate source ingestion, change capture, stream processing, batch processing, storage, serving and governance.
- Define event time, freshness, replay, ordering and correctness independently from throughput.
- Distinguish operational queries, interactive analytics, scheduled transformation and machine-learning feature production.
- Treat catalog, lineage, quality, access policy and cost attribution as platform capabilities.

## Architecture-changing questions

- Which sources and consumers exist, and is each flow batch, streaming or change-data capture?
- What freshness, replay horizon, ordering and late-data behavior does each dataset require?
- Is the primary serving pattern lakehouse analysis, cluster-based big data processing or a curated data product?
- Which datasets contain sensitive fields, and how must access follow data across derived tables?
- Who owns schema evolution, quality rules, lineage, backfills and failed-job recovery?
- Must the platform reuse an existing Hadoop ecosystem or minimize cluster operations?

## Product-family mappings

```yaml
products:
  - product_name: 大数据研发治理套件 DataLeap
    official_url: https://www.volcengine.com/docs/6260
    stable_capabilities: [data development, workflow orchestration, data governance, metadata and quality management]
    use_when: [teams need a managed environment for developing and governing shared data workflows]
    avoid_or_verify_when: [source and engine integrations are assumed, governance ownership and deployment model are undefined]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: E-MapReduce
    official_url: https://www.volcengine.com/docs/86403/1829870?lang=zh
    stable_capabilities: [managed big-data clusters, Hadoop ecosystem processing, Spark and related engine workloads]
    use_when: [existing ecosystem compatibility or cluster-level engine control is important]
    avoid_or_verify_when: [the team does not want cluster operations, required components or engine compatibility are unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 湖仓一体分析服务 LAS
    official_url: https://www.volcengine.com/docs/86403/1829870?lang=zh
    stable_capabilities: [lakehouse analytics, data-lake query and processing, shared analytical storage integration]
    use_when: [analytical workloads need a lakehouse-oriented managed service over shared data]
    avoid_or_verify_when: [table format, engine behavior or workload concurrency is unverified, operational transactions dominate]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 消息队列 Kafka版
    official_url: https://www.volcengine.com/docs/6439
    stable_capabilities: [Kafka-compatible message buffering, topic-based event ingestion, producer and consumer integration]
    use_when: [realtime events need durable decoupling, replayable consumption, or Kafka protocol compatibility]
    avoid_or_verify_when: [ordering, retention, partition count, network access, and client compatibility are unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 流式计算 Flink版
    official_url: https://www.volcengine.com/docs/6581
    stable_capabilities: [managed Flink stream processing, Flink SQL jobs, connector-based realtime computation]
    use_when: [event streams require stateful processing, enrichment, aggregation, CDC processing, or realtime ETL]
    avoid_or_verify_when: [connector support, state size, checkpoint behavior, and downstream compatibility are unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 日志服务 TLS
    official_url: https://docs.volcengine.com/docs/6470
    stable_capabilities: [log and event collection, storage, search analysis, alerting, dashboard visualization]
    use_when: [operational events or logs need managed ingestion, realtime search, analysis, alerting, or visualization]
    avoid_or_verify_when: [the data is not log/event shaped, custom schema governance or analytical warehouse semantics dominate]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: ByteHouse 企业版
    official_url: https://www.volcengine.com/docs/6464/152221
    stable_capabilities: [large-scale data storage, high-efficiency write, fast query analytics, warehouse serving]
    use_when: [dashboard or analytical serving needs a managed warehouse over high-volume event-derived tables]
    avoid_or_verify_when: [interactive BI concurrency, ingestion method, resource model, and workload isolation are unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
```

## Integration patterns

- Land immutable source data in object storage, then publish validated and curated layers with explicit ownership.
- Make ingestion replayable: preserve source offsets or checkpoints and make transformations idempotent.
- Use DataLeap to coordinate development and governance while the selected processing engine executes batch or lakehouse workloads.
- Separate compute from durable data where the selected engine supports it; do not let transient cluster storage become the only copy.
- Publish data products with schema contracts, freshness indicators, lineage and access policies.

## Review points

- Trace one record from source through retries, transformations, quality checks and each serving destination.
- Test schema evolution, duplicate delivery, late arrival, backfill and partial failure.
- Verify partitioning and file layout against actual query and update patterns.
- Confirm sensitive-field masking, row or column policy, audit evidence and deletion propagation.
- Define freshness, completeness, correctness, job recovery and cost metrics per data product.

## Dynamic facts to recheck

For every shortlisted product, recheck `region`, `price`, `specification`, `quota`, `SLA` and `version` in the official documentation for the target account and record the query date. Also recheck connectors, engine and table-format compatibility, scheduling and recovery behavior, catalog integration, security controls, storage integration and lifecycle notices.

## Official discovery links

- [DataLeap documentation](https://www.volcengine.com/docs/6260)
- [Volcano Engine documentation center](https://www.volcengine.com/docs/86403/1829870?lang=zh)
- [Object Storage documentation](https://www.volcengine.com/docs/6349)
- [Message Queue for Kafka documentation](https://www.volcengine.com/docs/6439)
- [Streaming Computing Flink documentation](https://www.volcengine.com/docs/6581)
- [TLS documentation](https://docs.volcengine.com/docs/6470)
- [ByteHouse Enterprise documentation](https://www.volcengine.com/docs/6464/152221)
