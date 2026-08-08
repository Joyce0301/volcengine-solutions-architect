建议采用“容器化 + 托管数据库/缓存 + 弹性伸缩”的最小改造方案：

```text
用户
  │
DNS / CDN / WAF
  │
公网负载均衡 CLB
  │
容器服务 VKE（多可用区）
  ├─ API 服务 Deployment（无状态、多副本、HPA）
  ├─ 异步消费者 / 定时任务
  └─ Ingress / 服务发现 / 配置管理
  │
  ├─ 云数据库 RDS（主备高可用，读写分离）
  ├─ Redis（会话、购物车、库存热点、限流）
  ├─ 消息队列（订单创建、支付回调、库存扣减、通知）
  ├─ 对象存储 TOS（商品图、附件、静态资源）
  └─ 日志服务 TLS + 监控告警
```

核心设计：

- API 尽量保持现有代码与接口不变，打包为 Docker 镜像后部署到 VKE；通过环境变量/配置中心替换数据库、Redis、对象存储连接地址。
- VKE 节点跨至少两个可用区部署，API 服务无状态化，设置健康检查、滚动发布和自动扩缩容。晚间突发流量按 CPU、QPS、延迟或队列堆积触发 HPA；节点池启用自动扩容。
- CLB 承接公网流量，前置 WAF 防护常见 Web 攻击；静态资源、图片和可缓存接口经 CDN 加速，降低源站压力。
- RDS 使用高可用主备架构；订单、支付等强一致写请求走主库，商品详情、订单查询等读流量通过只读实例分担。保留现有 ORM/JDBC，优先只改连接串和连接池参数。
- Redis 承担缓存、会话、分布式锁和热点库存；库存扣减应采用原子操作，并将最终落库通过消息队列异步化。
- 对订单、支付、发货、短信等链路引入消息队列，削峰填谷；消费者必须支持幂等、重试和死信处理，避免突发流量直接压垮数据库。
- 商品图片迁移到 TOS，经 CDN 分发；应用只需将原有本地文件路径替换为对象存储 SDK 或兼容 S3 的客户端。
- 使用 TLS 汇集应用日志、访问日志和审计日志，并按接口错误率、P95/P99 延迟、数据库连接数、Redis 命中率、消息积压、Pod/节点资源率建立告警。

迁移顺序建议：先容器化并在 VKE 灰度部署 → 接入 CLB/CDN/WAF → 迁移缓存和对象存储 → 迁移 RDS 并做数据校验 → 对订单等高峰链路引入消息队列 → 逐步放量、保留可回滚的旧环境。

## Baseline observations
- Requirements gap list before solution: FAIL
- Only architecture-changing questions: FAIL
- Facts separated from assumptions: FAIL
- Product alternatives and switch conditions: FAIL
- Security, reliability, observability, and cost covered: FAIL
- Official evidence and retrieval dates: FAIL
- Production-readiness claim appropriately bounded: PASS
