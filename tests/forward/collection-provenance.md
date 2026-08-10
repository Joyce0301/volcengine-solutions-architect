# Forward Collection Provenance

This manifest records the origin and current integrity hash of the forward fixtures. The six report fixtures originated in fresh child-agent reruns, then were mechanically normalized as the report contract evolved (canonical product labels, table columns, and validator compatibility). They are therefore maintained regression fixtures, not byte-for-byte raw model responses. `interview-behavior.json` is a deterministic conversation acceptance fixture and is not claimed as a fresh model execution.

## Controls applied

- Each listed run used a fresh child-agent session for that scenario.
- Children used the worktree-local Skill path `/Users/juice/Desktop/vibe coding/volcengine Architecture/.worktrees/volcengine-architecture-plugin/volcengine-architecture/skills/design-volcengine-architecture`.
- Children were instructed not to inspect `tests/baselines` or other agents' outputs.
- Report edits after collection are reviewable in Git; the current hashes below detect unrecorded fixture drift.
- Browsing was disabled; dynamic/current facts were either supported with official Volcengine URLs plus retrieval date in the same paragraph/table cell, or left as runtime-verification open items without concrete values.

## Persisted runs

| Scenario | Origin | Timestamp | Session log line | Literal scenario prompt | Current fixture SHA-256 |
| --- | --- | --- | --- | --- | --- |
| ai-agent | `/root/task7_forward/rerun_ai_agent_final` | 2026-08-09T06:35:05.250Z | `/Users/juice/.codex/sessions/2026/08/09/rollout-2026-08-09T11-40-29-019fe49b-9779-73a3-a915-f51c5457f955.jsonl:552` | 我们有约 3 万份内部制度和产品文档，想做一个能回答问题并调用工单系统的企业助手。请基于火山引擎设计架构。 | `3d1f43197e29a67d871aa41d71c1bde384ae3ceac50429731e6ff44114933efe` |
| cloud-native | `/root/complete_forward_validation/cloud_native_fix` | 2026-08-09T10:42:31.975Z | `/Users/juice/.codex/sessions/2026/08/09/rollout-2026-08-09T18-36-18-019fe618-4594-7161-bd1e-711d81a37ef2.jsonl:104` | 把一个日活 300 万、晚间有突发流量的电商 API 迁到火山引擎，要求尽量少改代码。请给出架构。 | `709a4e3323046119ac48d4cc01402cd60198572f93cf19e3bb67b5374d74c728` |
| intelligent-service | `/root/task7_forward/rerun_intelligent_service` | 2026-08-09T06:30:15.509Z | `/Users/juice/.codex/sessions/2026/08/09/rollout-2026-08-09T11-40-29-019fe49b-9779-73a3-a915-f51c5457f955.jsonl:524` | 构建支持电话和在线渠道的智能客服，需要语音识别、语音合成、知识问答、转人工和经营分析。 | `bdf00fe8ca19c74c33d04c61dbf2b02553c9c71eff7a1b7ce72c075782df6dea` |
| media | `/root/complete_forward_validation/media_fix` | 2026-08-09T10:42:42.767Z | `/Users/juice/.codex/sessions/2026/08/09/rollout-2026-08-09T18-36-18-019fe618-4594-7161-bd1e-711d81a37ef2.jsonl:112` | 设计一套面向全国用户的教育直播与回放平台，需要连麦、转码、内容审核和弱网体验保障。 | `2cfa67077752ea074ac0eaa08147eda4a82d17c49849e839db698d4e01a0cc97` |
| realtime-data | `/root/complete_forward_validation/realtime_data_fix` | 2026-08-09T10:42:18.169Z | `/Users/juice/.codex/sessions/2026/08/09/rollout-2026-08-09T18-36-18-019fe618-4594-7161-bd1e-711d81a37ef2.jsonl:96` | 我们需要汇总 App 埋点、交易和设备事件，支持分钟级运营看板和次日复杂分析。请设计火山引擎方案。 | `40cae8275b0520cae707e14315955b644d47aa71d7a7d31131ad40795a7a6875` |
| regulated-finance | `/root/complete_forward_validation/regulated_finance_fix` | 2026-08-09T10:43:02.527Z | `/Users/juice/.codex/sessions/2026/08/09/rollout-2026-08-09T18-36-18-019fe618-4594-7161-bd1e-711d81a37ef2.jsonl:120` | 某金融机构希望在火山引擎部署客户风险分析平台，数据敏感，要求专网接入、完整审计、同城容灾和异地备份。 | `8b3a55d48770218ac2ac3d10bcb861203d9103a7e0023bb354af2650b7e9076d` |

## Deterministic conversation fixture

| Fixture | Purpose | Current fixture SHA-256 |
| --- | --- | --- |
| `interview-behavior.json` | Vague prompt single-question entry, explicit default exit, and information-rich prompt direct report | `1780e0022adfef8827d8d93e2d163a44b473c3869019414f65cf3aa76dc3778f` |
