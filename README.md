# Volcengine Solutions Architect

一个 Codex 原生、可扩展的火山引擎架构设计 Plugin/Skill。它可以根据业务需求设计 AI、云原生、大数据、实时数据、数据库、存储、音视频、边缘计算、安全合规等架构。

GitHub: <https://github.com/Joyce0301/volcengine-solutions-architect>

## 安装

在 Codex 的插件安装入口中，从 GitHub 安装：

```text
Joyce0301/volcengine-solutions-architect
```

插件清单位于仓库中的 `volcengine-architecture/.codex-plugin/plugin.json`。

## 触发方式

### 显式触发（推荐）

Skill 名称是 `$design-volcengine-architecture`：

```text
$design-volcengine-architecture

我们要建设一个面向企业内部员工的智能知识助手。

- 用户规模：1 万名员工
- 文档规模：约 3 万份
- 支持企业微信和 Web
- 需要知识问答、工单查询和工单创建
- 敏感数据不能出公网
- 先做 PoC，再逐步上线
- 希望全部基于火山引擎
```

### 自然语言触发

以下类型的请求也会匹配该 Skill：

```text
请帮我基于火山引擎设计一个电商系统架构。
```

```text
请把现有 Kubernetes 系统迁移到火山引擎，并给出产品选型、网络架构、容灾和成本考虑。
```

如果希望触发结果稳定，建议显式写出 `$design-volcengine-architecture`。

## 推荐调用模板

```text
$design-volcengine-architecture

请基于火山引擎设计一套架构。

业务目标：
<要解决什么问题>

用户与流量：
<用户数、并发量、峰值、增长预期>

核心功能：
<功能列表>

数据：
<数据类型、数据量、冷热数据、保留周期>

性能要求：
<延迟、吞吐、实时性>

可靠性：
<可用性、容灾、RTO、RPO>

安全合规：
<私网、数据隔离、等保、审计、跨境限制>

部署要求：
<公有云、专有网络、混合云、迁移现有系统>

成本：
<预算、成本敏感点>

交付形式：
请输出产品选型、逻辑架构、部署拓扑、端到端数据流、风险清单、PoC 计划和生产 readiness 评估。
```

信息不完整时，也可以只给业务目标：

```text
$design-volcengine-architecture

我要做一个面向短视频平台的实时推荐系统。
```

Skill 会先列出需求缺口，再只追问会改变架构的关键问题。

## 工作流程

Skill 通常按以下顺序工作：

1. 先输出 `Requirements gap check`，区分已知事实、架构缺口和假设。
2. 自适应地逐题澄清，每轮只问一个会改变架构的问题；信息充分时自动停止，最多八题，也可以要求按默认假设继续。
3. 自动识别 AI/Agent、云原生、大数据、实时数据、数据库与存储、音视频、边缘计算、金融与合规等场景。
4. 加载对应的火山引擎产品参考资料。
5. 必要时执行需求分析、产品研究、领域架构、安全可靠性和 FinOps 等内部角色审查。
6. 把每项关键能力映射到具体火山引擎产品，并输出产品职责、备选方案、切换条件、逻辑架构、部署拓扑、端到端数据流、容灾、安全、成本和实施路线。
7. 对价格、规格、配额、SLA、可用地域、版本状态等动态信息要求官方证据和查询日期。
8. 输出 `Production readiness: READY` 或 `Production readiness: NOT READY`，并说明未就绪原因。

完成架构关键问题澄清后，Skill 会把最终架构结果、产品依据、数据流、部署与容灾细节、风险和验收标准写入 Markdown 报告。默认路径为 `reports/volcengine-architecture-report.md`；也可以在请求中指定报告路径。报告是交付源文件，聊天消息只返回摘要和报告绝对路径。

除最前面的需求缺口检查外，最终方案包含以下十二个部分：

1. Executive summary
2. Known facts, assumptions, and open items
3. Routing record
4. Architecture decisions
5. Logical architecture
6. Deployment topology
7. End-to-end data flow
8. Volcengine product mapping
9. Non-functional design
10. Implementation roadmap
11. Risk and validation plan
12. Completeness score

## 设计边界

这个 Skill 负责架构设计、产品选型、方案评审和交付物校验，不会自动：

- 创建火山引擎云资源
- 执行 Terraform 或变更线上网络
- 购买实例或开通服务
- 在没有官方证据时编造价格、SLA、配额或规格

通过 Skill 输出的 `READY` 只是有边界的架构建议，不等同于部署授权。关键需求、官方证据、安全控制、RTO/RPO、成本驱动因素或运维责任人未确认时，方案会标记为 `NOT READY`。

## 目录结构

```text
volcengine-architecture/
├── .codex-plugin/plugin.json
└── skills/design-volcengine-architecture/
    ├── SKILL.md
    ├── references/
    └── scripts/validate-deliverable.py
```

如需了解完整契约、产品参考资料和验证规则，请阅读 [SKILL.md](volcengine-architecture/skills/design-volcengine-architecture/SKILL.md)。
