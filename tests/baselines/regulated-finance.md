建议采用“生产同城双活/容灾 + 异地备份 + 专网隔离”的分层架构：

- 接入层：通过专线/VPN 接入火山引擎 VPC，使用多个可用区部署负载均衡与应用网关；公网入口默认关闭，仅保留受控运维访问。
- 网络与隔离：生产、数据、管理、灾备划分独立 VPC/子网与安全组；以最小权限控制东西向访问，并通过网络 ACL、私有访问和堡垒机强化边界。
- 计算层：风险分析应用部署在容器平台或弹性计算集群，跨两个同城可用区多副本运行；服务无状态化，配置与密钥集中托管。
- 数据层：核心交易/客户数据采用高可用数据库，跨可用区同步复制；缓存、消息队列和对象存储均启用多副本与加密。风险模型训练与批处理同生产交易链路隔离。
- 同城容灾：关键应用、数据库和中间件在同城双可用区部署，设定明确 RTO/RPO；定期演练故障切换、回切及数据一致性校验。
- 异地备份：将数据库备份、对象数据和审计日志按策略复制至异地区域，采用不可变/防篡改备份、生命周期管理和定期恢复演练；异地副本可满足较长 RPO 的灾难恢复需求。
- 安全与审计：全链路 TLS、静态数据加密、密钥托管与轮换；所有控制台/API/运维操作、网络访问、数据库审计和应用日志统一汇聚到日志与审计平台，设置长期留存、检索告警与防篡改存档。
- 运维与合规：通过 IAM 实施 RBAC、MFA 和职责分离；使用堡垒机进行运维审计；建立基线扫描、漏洞管理、告警响应、备份恢复和容灾演练制度。

建议先与合规、业务连续性和安全团队共同明确数据分级、审计留存期限、RTO/RPO、密钥管理边界及异地数据合规要求，再据此确定具体产品规格与部署拓扑。

## Baseline observations
- Requirements gap list before solution: FAIL
- Only architecture-changing questions: FAIL
- Facts separated from assumptions: FAIL
- Product alternatives and switch conditions: FAIL
- Security, reliability, observability, and cost covered: FAIL
- Official evidence and retrieval dates: FAIL
- Production-readiness claim appropriately bounded: PASS
