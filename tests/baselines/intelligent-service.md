可采用“全渠道接入 + AI 对话中台 + 人工协同 + 数据分析”的架构：

- 电话渠道：通过呼叫中心/SIP 接入，实时语音识别（ASR）将来电转文字；由大模型结合知识库进行理解、问答与流程编排；语音合成（TTS）将回复播报给用户。
- 在线渠道：网页、App、微信等通过统一客服 API 接入，直接调用同一套大模型问答、会话管理和工单能力，保证不同渠道答案一致。
- 知识问答：将 FAQ、产品文档、工单记录等清洗切分后写入知识库与向量库；采用 RAG 检索增强生成，并设置知识版本、审核、引用来源和低置信度兜底策略。
- 转人工：基于用户主动请求、意图识别、情绪/投诉风险、连续未解决或低置信度触发转接；同时将用户信息、会话摘要、已检索知识和处理轨迹同步给坐席，避免重复描述。
- 经营分析：采集通话录音、转写文本、在线会话、排队与工单数据，分析咨询量、接通率、解决率、转人工率、首响时长、满意度、热点问题与机器人命中率；使用实时看板和离线数仓支持运营复盘。

在火山引擎上可组合使用语音识别/语音合成、豆包大模型与模型服务平台、知识库/RAG 能力、消息队列与 API 网关，以及日志分析和数据仓库产品。敏感数据应脱敏、加密存储并实施权限审计；生产环境需配置多可用区、高可用降级和人工坐席兜底。

## Baseline observations
- Requirements gap list before solution: FAIL
- Only architecture-changing questions: FAIL
- Facts separated from assumptions: FAIL
- Product alternatives and switch conditions: FAIL
- Security, reliability, observability, and cost covered: FAIL
- Official evidence and retrieval dates: FAIL
- Production-readiness claim appropriately bounded: FAIL
