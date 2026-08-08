推荐采用“实时湖仓一体 + 离线数仓”的分层方案：

```text
App 埋点 / 交易系统 / 设备事件
        ↓
  Kafka（统一事件总线）
        ↓
Flink 实时计算 ─────────→ ByteHouse 实时明细与聚合 → 分钟级运营看板
        ↓
   TOS 数据湖（原始数据、ODS）
        ↓
 EMR / DataLeap 离线 ETL、建模
        ↓
 ByteHouse 数仓宽表 / 主题库 → 次日复杂分析、BI、自助取数
```

核心组件：

- 接入层：App 通过增长分析/埋点 SDK 或 HTTP 接入；交易与设备侧通过 Kafka Producer、日志采集或 CDC 同步进入 Kafka。
- 消息与缓冲：使用消息队列 Kafka 按事件类型拆分 Topic，按用户、设备或订单 ID 分区；保留原始事件用于重放。
- 实时层：使用托管 Flink 完成清洗、去重、事件时间窗口聚合、维表关联和异常数据旁路。
  - 分钟级指标：PV/UV、转化漏斗、GMV、订单量、支付成功率、活跃设备数、设备告警数等。
  - 将实时明细和分钟/小时聚合结果写入 ByteHouse。
- 实时看板：ByteHouse 作为 OLAP 查询引擎，接入 DataWind 或企业现有 BI；高频看板优先查询预聚合表，必要时加缓存。
- 数据湖：原始 Kafka 数据同时沉淀至 TOS，使用 Parquet/ORC，并按 `dt/hour/event_type` 分区，作为低成本可追溯底座。
- 次日离线分析：通过 EMR Spark/Flink SQL 或 DataLeap 调度，完成用户、订单、设备主题域建模，产出 DWD、DWS、ADS 分层数据；复杂明细与宽表写入 ByteHouse。
- 数据治理：DataLeap 负责元数据、血缘、质量校验、任务编排和权限；敏感字段在入湖/入仓前脱敏或加密。

关键设计要点：

- 统一事件规范：`event_id`、`event_time`、`user_id`、`device_id`、`order_id`、事件属性、来源与版本号；交易事件必须包含幂等键。
- 实时准确性：Flink 开启 checkpoint 与 exactly-once；消费端按 `event_id` 去重，并处理迟到数据和撤销/退款等修正事件。
- 热冷分层：近 7～30 天明细保留 ByteHouse 热存储，长期原始数据留在 TOS；复杂历史回溯优先从湖上计算。
- 维表策略：商品、渠道、设备型号等低频变更维表可通过 Redis/HBase 或 ByteHouse 字典表实时关联；高频变更维表通过 CDC 维护。
- 容灾与监控：Kafka 多副本、Flink checkpoint 存 TOS、ByteHouse 副本与分区；监控消费积压、任务延迟、数据量突变、空值率、重复率和指标对账差异。

建议的数据分层：

- ODS：原始埋点、交易、设备事件。
- DWD：统一清洗后的行为、订单、支付、设备状态明细。
- DWS：用户、商品、渠道、设备等主题汇总。
- ADS：运营大盘、漏斗、交易监控、设备健康度等直接服务表。

这样可在分钟级满足运营看板时效，同时保留完整原始数据与规范主题模型，支持次日多维钻取、归因、漏斗、留存、设备故障关联和交易分析。

## Baseline observations
- Requirements gap list before solution: FAIL
- Only architecture-changing questions: FAIL
- Facts separated from assumptions: FAIL
- Product alternatives and switch conditions: FAIL
- Security, reliability, observability, and cost covered: FAIL
- Official evidence and retrieval dates: FAIL
- Production-readiness claim appropriately bounded: FAIL
