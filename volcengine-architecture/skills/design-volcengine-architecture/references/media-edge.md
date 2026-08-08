# Media and Edge

## Capability decomposition

- Separate media ingest, asset management, processing, origin storage, distribution, playback and quality monitoring.
- Distinguish one-to-many live delivery, on-demand playback and many-to-many real-time communication.
- Treat image pipelines, generic content caching, media delivery and edge compute as different operating models.
- Model rights protection, moderation, access control and origin protection across the full content lifecycle.

## Architecture-changing questions

- Is the user experience live, on demand, interactive real time, image-centric or generic web/download delivery?
- Where are users and origins, and which latency, startup, quality and interactivity outcomes matter?
- Which devices, SDKs, codecs, containers and playback protocols must be supported?
- Which transformations occur synchronously, asynchronously, at origin or at the edge?
- What recording, retention, moderation, watermark, authorization and copyright controls apply?
- Is edge code required, or can cache rules and managed media workflows satisfy the need?

## Product-family mappings

```yaml
products:
  - product_name: 内容分发网络 CDN
    official_url: https://www.volcengine.com/docs/6454
    stable_capabilities: [edge content caching, web and download acceleration, origin fetch, domain and cache control]
    use_when: [cacheable content needs distributed delivery, origin load and user access latency should be reduced]
    avoid_or_verify_when: [content is predominantly uncacheable or bidirectional, origin protection and cache-key design are unresolved]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 视频点播
    official_url: https://www.volcengine.com/docs/4
    stable_capabilities: [media upload and asset management, media processing, on-demand distribution and playback, quality monitoring]
    use_when: [recorded media needs an end-to-end managed workflow and playback delivery]
    avoid_or_verify_when: [the flow is primarily live or interactive, codec and player compatibility are unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 视频直播
    official_url: https://www.volcengine.com/docs/6469
    stable_capabilities: [live stream ingest, live media processing, live distribution and playback, recording and monitoring]
    use_when: [one-to-many live broadcasting and managed live workflows are required]
    avoid_or_verify_when: [the experience requires many-to-many interaction, ingest and playback protocol support is unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 实时音视频 veRTC
    official_url: https://www.volcengine.com/docs/6348
    stable_capabilities: [real-time audio and video communication, client SDK integration, room and session control, quality monitoring]
    use_when: [participants need interactive audio or video with real-time session behavior]
    avoid_or_verify_when: [one-way broadcast or file playback is sufficient, target client and network support are unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: veImageX
    official_url: https://www.volcengine.com/docs/508
    stable_capabilities: [image upload and asset management, image processing, image distribution, client delivery and quality tooling]
    use_when: [applications need a managed image lifecycle from upload through processing and delivery]
    avoid_or_verify_when: [generic object delivery is sufficient, image format and client SDK requirements are unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 边缘计算节点
    official_url: https://www.volcengine.com/docs/6499
    stable_capabilities: [distributed edge compute, edge application deployment, edge networking and load distribution]
    use_when: [application processing must run closer to users or data sources than central cloud resources]
    avoid_or_verify_when: [CDN rules or central compute meet the latency need, workload portability and node coverage are unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: TrafficRoute DNS 套件
    official_url: https://www.volcengine.com/docs/6758
    stable_capabilities: [authoritative and private DNS, traffic steering, health-aware routing, domain resolution management]
    use_when: [multi-endpoint or multi-site delivery needs DNS-based traffic routing and failover]
    avoid_or_verify_when: [DNS caching behavior is incompatible with the recovery objective, resolver and routing policy support are unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
```

## Integration patterns

- For on-demand media, ingest into the managed asset workflow, process asynchronously, distribute through the service delivery path and surface playback telemetry.
- For live broadcast, separate publisher ingest, processing, origin, distribution, player authorization and optional recording-to-on-demand.
- Use veRTC for interactive rooms; bridge to broadcast delivery only when audience scale and interaction roles require distinct paths.
- Place TOS or the managed media asset store behind the delivery service, with signed access and origin protection appropriate to the content.
- Use TrafficRoute for DNS-level steering and edge compute only for logic that must execute near users; keep durable state in regional services.

## Review points

- Test representative devices, networks, media formats and failover paths.
- Validate cache keys, invalidation, origin shielding, signed access and hot-content behavior.
- Define retry, idempotency and event handling for upload, transcoding, recording and callback workflows.
- Confirm moderation points, rights controls, retention, deletion and audit evidence.
- Make quality metrics user-facing: startup, rebuffering, interaction delay, publish success and processing failure.

## Dynamic facts to recheck

For every shortlisted product, recheck `region`, `price`, `specification`, `quota`, `SLA` and `version` in the official documentation for the target account and record the query date. Also recheck node coverage, protocols, codecs, SDK platforms, processing templates, storage and retention behavior, security features, moderation integrations and service-to-service compatibility.

## Official discovery links

- [CDN documentation](https://www.volcengine.com/docs/6454)
- [Video on Demand documentation](https://www.volcengine.com/docs/4)
- [Live Video documentation](https://www.volcengine.com/docs/6469)
- [veRTC documentation](https://www.volcengine.com/docs/6348)
- [veImageX documentation](https://www.volcengine.com/docs/508)
- [Edge Computing Node documentation](https://www.volcengine.com/docs/6499)
- [TrafficRoute documentation](https://www.volcengine.com/docs/6758)
