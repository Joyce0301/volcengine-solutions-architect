采用“多地域接入 + 中央控制面 + 媒体处理流水线”的架构，直播链路与回放链路分离，核心目标是低延迟连麦、高并发观看、合规审核和弱网可用。

```text
教师/学生端
  ├─ 直播推流：RTMP / WebRTC
  ├─ 连麦互动：WebRTC
  └─ 回放观看：HLS / DASH
        ↓
全国边缘接入与调度
  ├─ 就近接入、智能 DNS、全局负载均衡
  ├─ CDN 边缘分发
  └─ 多线路、跨运营商调度
        ↓
媒体中心
  ├─ 实时转码与多码率输出
  ├─ 直播录制、切片、存储
  ├─ 内容审核
  └─ 直播流分发
        ↓
业务控制面
  ├─ 课程、班级、房间、排课
  ├─ 鉴权、付费与权限
  ├─ 信令、IM、白板、互动数据
  └─ 监控、告警、运营分析
```

- 直播观看：教师使用 RTMP 或 WebRTC 推流；大规模学生观看优先走 HLS/LL-HLS + CDN。热门课程预热 CDN，回源采用源站集群与多活容灾。
- 连麦：采用 WebRTC + SFU 架构。教师、助教和少量学生进入互动房间，SFU 按订阅关系转发音视频，避免 MCU 混流造成高成本和高延迟。课堂主画面可同步转为 CDN 直播流，供大量旁听用户观看。
- 转码：将源流实时转成 1080p、720p、480p、360p 等多档码率，视频使用 H.264/H.265（按终端兼容性选择），音频 AAC/Opus。支持横竖屏、截图、水印、字幕和录制。
- 回放：直播同时录制为分段文件，生成 HLS/DASH 回放清单；原始文件存对象存储，热点回放由 CDN 分发，冷数据通过生命周期策略转低成本存储。
- 内容审核：直播流进行实时涉黄、涉暴、涉政、广告与语音文本审核；命中高风险内容时支持自动断流、切换垫片、人工复审和审计留档。回放在发布前再做一次离线全量审核。
- 弱网保障：
  - WebRTC 启用自适应码率、丢包重传、FEC、带宽探测、音频优先和动态降帧/降分辨率。
  - 观看端支持多码率 ABR、首屏低码率、CDN 就近节点、预加载与断线续播。
  - 网络极差时自动退化为“仅音频 + 课件/白板”，连麦失败可降级为语音连麦或文字互动。
  - 客户端采集网络质量、卡顿率、首帧时间、丢包和端到端延迟，驱动线路切换和质量告警。
- 业务服务：课程、用户、订单、排课等采用微服务；缓存用于课程页和鉴权信息；消息队列承接直播状态、审核事件、录制完成和异步通知。房间信令和在线状态使用高可用长连接集群。
- 安全与权限：播放 URL 使用短期签名、Token 鉴权、防盗链、DRM/加密 HLS；教师、助教、学生、旁听者按角色授权；对敏感课程实施录屏水印和访问审计。
- 高可用：控制面跨地域多活，媒体服务按地域部署；直播源支持主备推流和跨区域容灾；对象存储跨区域复制；关键指标包括推流成功率、首帧时间、卡顿率、连麦成功率、互动延迟、审核命中与 CDN 回源率。

## Baseline observations
- Requirements gap list before solution: FAIL
- Only architecture-changing questions: FAIL
- Facts separated from assumptions: FAIL
- Product alternatives and switch conditions: FAIL
- Security, reliability, observability, and cost covered: PASS
- Official evidence and retrieval dates: FAIL
- Production-readiness claim appropriately bounded: FAIL
