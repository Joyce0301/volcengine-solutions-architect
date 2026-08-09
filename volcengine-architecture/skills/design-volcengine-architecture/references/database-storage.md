# Database and Storage

## Capability decomposition

- Choose data semantics first: relational transactions, document access, key-value/cache, object access or shared filesystem.
- Separate system-of-record durability from acceleration layers and derived copies.
- Model access pattern, consistency, transaction scope, index shape, object size distribution and lifecycle independently.
- Design backup, restore, replication, encryption, retention and deletion as explicit flows.

## Architecture-changing questions

- Which data store is authoritative, and what consistency or transaction boundary must it preserve?
- Does the application require MySQL, PostgreSQL, MongoDB or Redis protocol behavior, and which extensions or commands does it depend on?
- Is storage accessed as objects or as a mounted shared filesystem?
- What RTO, RPO, retention, legal-hold and deletion requirements apply?
- Will migration require continuous change replication, dual writes or a maintenance window?
- Must compute and data remain on private networks or within a specified residency boundary?

## Product-family mappings

```yaml
products:
  - product_name: 云数据库 MySQL 版
    official_url: https://www.volcengine.com/docs/6313
    stable_capabilities: [managed relational database, MySQL-compatible access, backup and recovery, monitoring]
    use_when: [the application requires managed MySQL semantics, operational database administration should be delegated]
    avoid_or_verify_when: [the workload depends on unsupported MySQL behavior, the target topology or recovery design is not confirmed]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 云数据库 veDB MySQL 版
    official_url: https://www.volcengine.com/docs/6357
    stable_capabilities: [cloud-native relational database, MySQL-compatible access, read scaling, backup and recovery]
    use_when: [a cloud-native MySQL-compatible architecture is preferred, read scaling and managed operations are material]
    avoid_or_verify_when: [application compatibility has not been tested, consistency or endpoint behavior is assumed]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 云数据库 PostgreSQL 版
    official_url: https://www.volcengine.com/docs/6438
    stable_capabilities: [managed relational database, PostgreSQL-compatible access, backup and recovery, monitoring]
    use_when: [the application requires PostgreSQL semantics, managed relational operations are desired]
    avoid_or_verify_when: [required extensions or engine behavior are unverified, migration compatibility is unknown]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 缓存数据库 Redis 版
    official_url: https://www.volcengine.com/docs/6293
    stable_capabilities: [managed in-memory data service, Redis-compatible access, caching, replication and recovery operations]
    use_when: [low-latency key-value access is required, cache or transient coordination state is appropriate]
    avoid_or_verify_when: [Redis is being treated as the sole durable system of record without recovery analysis, command compatibility is assumed]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 文档数据库 MongoDB 版
    official_url: https://www.volcengine.com/docs/6447
    stable_capabilities: [managed document database, MongoDB-compatible access, replica and sharded architectures, backup and recovery]
    use_when: [document-oriented access and MongoDB protocol compatibility match the domain model]
    avoid_or_verify_when: [application features or drivers have not been compatibility-tested, sharding keys are unresolved]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 对象存储 TOS
    official_url: https://www.volcengine.com/docs/6349
    stable_capabilities: [object storage, bucket and object management, API and SDK access, lifecycle and access control]
    use_when: [unstructured data needs object semantics, durable media or data-lake storage is required]
    avoid_or_verify_when: [the workload requires filesystem semantics, access pattern and lifecycle cost have not been modeled]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 弹性文件存储
    official_url: https://www.volcengine.com/docs/6453
    stable_capabilities: [managed shared filesystem, file-protocol access, shared access from compute and containers]
    use_when: [multiple workloads require mounted shared file semantics, application changes for object storage are impractical]
    avoid_or_verify_when: [object semantics would suffice, protocol compatibility or workload I/O shape is unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
```

## Integration patterns

- Keep transactional state in a relational or document store; place cache in front only with an explicit invalidation and failure policy.
- Store large immutable artifacts in TOS and retain identifiers plus metadata in the operational database.
- Mount elastic file storage only for workloads that need shared filesystem behavior; do not use a mount as an implicit cross-region replication plan.
- Keep application-to-database paths private, scope identities narrowly, and route audit and service logs to the observability design.
- For migration, separate schema conversion, baseline copy, change replication, cutover validation and rollback.

## Review points

- Validate data model and protocol compatibility with a representative workload.
- Test restore, point-in-time recovery assumptions and application reconnection behavior.
- Check hot keys, skewed partitions, large objects, index growth and connection-pool behavior.
- Confirm encryption ownership, key rotation, backup access and deletion propagation.
- Record which layer owns retries, idempotency and cache consistency.

## Dynamic facts to recheck

For every shortlisted product, recheck `region`, `price`, `specification`, `quota`, `SLA` and `version` in the official documentation for the target account and record the query date. Also recheck engine compatibility, supported extensions or commands, storage classes, access protocols, backup retention, replication modes and migration support.

## Official discovery links

- [MySQL documentation](https://www.volcengine.com/docs/6313)
- [veDB MySQL documentation](https://www.volcengine.com/docs/6357)
- [PostgreSQL documentation](https://www.volcengine.com/docs/6438)
- [Redis documentation](https://www.volcengine.com/docs/6293)
- [MongoDB documentation](https://www.volcengine.com/docs/6447)
- [Object Storage documentation](https://www.volcengine.com/docs/6349)
- [Elastic File Storage documentation](https://www.volcengine.com/docs/6453)
