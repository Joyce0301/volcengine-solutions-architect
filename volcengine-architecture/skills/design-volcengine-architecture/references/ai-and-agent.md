# AI and Agent

## Capability decomposition

- Separate model capability from model serving, evaluation, adaptation, retrieval and agent orchestration.
- Treat prompts, tools, knowledge, memory, guardrails and human approval as independently governed components.
- Design grounding data ingestion, indexing, retrieval and citation as a data lifecycle.
- Keep model choice replaceable behind application-owned interfaces and evaluation gates.

## Architecture-changing questions

- Is the workload generation, understanding, embedding, multimodal processing, retrieval or an agent workflow?
- Which decisions may the model make, which tools may it call, and where is human approval mandatory?
- Is enterprise knowledge required, how fresh must it be, and what permissions must retrieval preserve?
- What data may leave the application boundary, be retained, or be used during customization?
- Which quality, latency, safety and cost metrics decide model or workflow selection?
- Is managed agent construction sufficient, or is application-owned orchestration required?

## Product-family mappings

```yaml
products:
  - product_name: 豆包大模型
    official_url: https://www.volcengine.com/product/doubao-dy
    stable_capabilities: [language and multimodal model families, generation and understanding, API-consumable model capability]
    use_when: [the application needs a first-party foundation-model family, model modality matches the workload]
    avoid_or_verify_when: [a named model variant is assumed without evaluation, data handling or modality support is unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 火山方舟
    official_url: https://www.volcengine.com/docs/82379/66619f8df281250274ef4f88?lang=zh
    stable_capabilities: [managed model access, model inference, evaluation, model customization, AI application development support]
    use_when: [teams need a managed model lifecycle and a common access layer for model-backed applications]
    avoid_or_verify_when: [required model or feature availability is assumed, the workload requires unsupported deployment control]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 扣子
    official_url: https://www.volcengine.com/sem
    stable_capabilities: [AI agent development, workflow and tool orchestration, knowledge-connected applications]
    use_when: [a managed agent-building experience can accelerate application delivery]
    avoid_or_verify_when: [runtime isolation or orchestration control requirements are unverified, production governance is undefined]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: HiAgent
    official_url: https://www.volcengine.com/sem
    stable_capabilities: [enterprise AI agent platform, agent construction and management, enterprise knowledge integration]
    use_when: [an enterprise-managed agent platform and centralized governance are required]
    avoid_or_verify_when: [tenant isolation, connector support or deployment model is assumed]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: VikingDB 向量数据库
    official_url: https://www.volcengine.com/sem
    stable_capabilities: [vector storage and retrieval, similarity search, multimodal retrieval support]
    use_when: [semantic retrieval is required for grounding, recommendation or similarity workflows]
    avoid_or_verify_when: [embedding compatibility, metadata filtering or freshness behavior is unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 火山方舟语音模型
    official_url: https://www.volcengine.com/docs/82379/2516286
    stable_capabilities: [speech synthesis, speech recognition, HTTP and WebSocket model access]
    use_when: [intelligent applications need managed ASR or TTS through a model access layer]
    avoid_or_verify_when: [audio format, streaming behavior, model availability, and data-handling terms are unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 豆包语音
    official_url: https://www.volcengine.com/docs/6561/1354869
    stable_capabilities: [streaming speech recognition, speech synthesis model documentation, WebSocket ASR access]
    use_when: [voice-first services need ASR or TTS model capabilities with direct voice APIs]
    avoid_or_verify_when: [language support, voice selection, latency target, commercial terms, and account enablement are unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
```

## Integration patterns

- Put an application-owned gateway between clients and model endpoints for authentication, policy, routing and observability.
- Build retrieval as ingestion and permission filtering to embedding and indexing, then query, reranking, citation and feedback.
- Give agents narrowly scoped tools with typed inputs, idempotency controls, timeouts and explicit approval for consequential actions.
- Evaluate model and prompt changes on a versioned task set before promotion; retain a rollback path.
- Keep conversation state, enterprise records and audit evidence in stores selected for their own durability and access requirements.

## Review points

- Define evaluation sets and acceptance thresholds for task quality, groundedness, safety and latency.
- Verify authorization at retrieval time and again at tool execution time.
- Test prompt injection, data exfiltration, unsafe tool use and untrusted retrieved content.
- Capture model, prompt, retrieval and tool versions in traces without logging prohibited data.
- Define graceful degradation for model timeout, refusal, retrieval miss and tool failure.

## Dynamic facts to recheck

For every shortlisted product, recheck `region`, `price`, `specification`, `quota`, `SLA` and `version` in the official documentation for the target account and record the query date. Also recheck available models and modalities, context and input limits, customization methods, endpoint behavior, data-handling terms, safety controls, connector support and model lifecycle notices.

## Official discovery links

- [Volcano Engine AI cloud overview](https://www.volcengine.com/sem)
- [Doubao model product page](https://www.volcengine.com/product/doubao-dy)
- [Ark documentation](https://www.volcengine.com/docs/82379/66619f8df281250274ef4f88?lang=zh)
- [Ark voice model access documentation](https://www.volcengine.com/docs/82379/2516286)
- [Doubao streaming ASR documentation](https://www.volcengine.com/docs/6561/1354869)
