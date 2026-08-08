# Skill-Free Baseline Collection Provenance

This manifest records the independent baseline collection runs that produced the six raw response sections in this directory. It is retained with the evidence package so the required fresh-agent and no-workspace-inspection controls are auditable.

## Controls applied to every run

- Each listed agent was a separate fresh child-agent session.
- Each received only the fixed prompt below plus the matching literal scenario prompt; no previous baseline response or task-design context was supplied.
- Every agent was instructed not to inspect workspace files, design documents, tests, or other artifacts, and not to use a specialized Volcengine architecture Skill.
- The raw response is the content before `## Baseline observations` in its matching baseline file. The SHA-256 value below is calculated over that raw section, including its trailing newline.

```text
请直接完成下面的用户请求。当前没有可用的专用火山引擎架构 Skill。不要查看工作区中的设计文档或其他测试输出。

```

## Runs

| Scenario | Fresh agent session | Literal scenario prompt | Raw response SHA-256 |
| --- | --- | --- | --- |
| ai-agent | `baseline_ai_agent` | 我们有约 3 万份内部制度和产品文档，想做一个能回答问题并调用工单系统的企业助手。请基于火山引擎设计架构。 | `340839c105698b549bb9e87b127beff280fd99f93f20093511918ef43c42037a` |
| cloud-native | `baseline_cloud_native` | 把一个日活 300 万、晚间有突发流量的电商 API 迁到火山引擎，要求尽量少改代码。请给出架构。 | `8bea13ffcf1672764d1d8a626caf568878a4f8343b4c0cd6fdfe69f694518ba8` |
| realtime-data | `baseline_realtime_data` | 我们需要汇总 App 埋点、交易和设备事件，支持分钟级运营看板和次日复杂分析。请设计火山引擎方案。 | `f24b0848be39e3f75f24ec8dda2af56a60f38171758a3e04e1da9eaaf546c1b4` |
| media | `baseline_media` | 设计一套面向全国用户的教育直播与回放平台，需要连麦、转码、内容审核和弱网体验保障。 | `4146a6776f9a45a243ee526ab874cb5fd7eef3be69aba19dcabceab018e3ccd1` |
| intelligent-service | `baseline_intelligent_service` | 构建支持电话和在线渠道的智能客服，需要语音识别、语音合成、知识问答、转人工和经营分析。 | `63dce975e47d0a11e33c1e47a8d98bb96c536b299a6fe6dc7274c964c36f0fb1` |
| regulated-finance | `baseline_regulated_finance` | 某金融机构希望在火山引擎部署客户风险分析平台，数据敏感，要求专网接入、完整审计、同城容灾和异地备份。 | `55a3e06d0d91a86bbbc8690e9d75f850ce5e1c854e379e40563002e1dabbc230` |

## Reproduction check

```bash
for f in tests/baselines/{ai-agent,cloud-native,realtime-data,media,intelligent-service,regulated-finance}.md; do
  printf '%s ' "$f"
  sed '/^## Baseline observations$/,$d' "$f" | shasum -a 256 | cut -d ' ' -f1
done
```
