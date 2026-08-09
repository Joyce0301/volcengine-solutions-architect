# Repository Agent Instructions

## Local-only architecture diagrams

架构图、拓扑图、PNG/PDF/SVG 渲染结果和对应的视觉设计哲学，默认属于本地临时交付物，不属于 GitHub 代码仓库交付物。

生成这类文件时必须遵守：

- 默认保存到本地临时目录或被 `.gitignore` 忽略的目录。
- 不要将架构图、渲染图、设计哲学文件加入 Git 暂存区。
- 不要提交或推送架构图相关文件。
- 不要为了展示图片而修改 README、插件清单或其他需要发布的文档并加入图片链接。
- 可以在当前对话中使用绝对路径展示本地图片。
- 只有用户明确要求“把这张图发布到 GitHub/提交到仓库”时，才允许将指定图文件加入版本控制。
- 即使用户要求发布，也必须先确认具体文件、目标仓库和目标分支；不能因普通的 Skill/代码推送请求而顺带发布架构图。

推荐本地输出位置：

```text
/tmp/volcengine-architecture-artifacts/
```

如果必须在仓库目录中生成，使用以下被忽略目录：

```text
docs/local-architecture-artifacts/
```

## Git 边界

“生成架构图”与“推送代码/Skill”是两个独立动作。执行代码或 Skill 发布时，必须检查 `git status`，确认架构图文件没有被暂存；除非用户明确授权，不得把本地视觉产物包含在发布范围内。
