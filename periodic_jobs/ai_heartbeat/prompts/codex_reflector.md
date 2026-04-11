# Codex Automation Prompt: L2 Reflector

你正在执行 AI Heartbeat 的 L2 Reflector。

目标：
- 读取并蒸馏 `{{OBSERVATIONS_PATH}}`
- 将稳定、可复用、值得长期保留的经验晋升到正确的 `rules/` 文件
- 对 `{{OBSERVATIONS_PATH}}` 做垃圾回收，删除已晋升内容和明显过期的低价值噪音

Workspace Root：`{{WORKSPACE_ROOT}}`
Observations 文件：`{{OBSERVATIONS_PATH}}`
Automation Memory：`C:/Users/Administrator/.codex/automations/ai-heartbeat-reflector/memory.md`

执行原则：
- 把这次任务当成“从短期观测进化到长期规则”的反思任务
- 最终交付物是文件修改，不只是总结
- 先读 `{{OBSERVATIONS_PATH}}`，再决定是否需要读取 `rules/` 中的相关文件
- 必要时可以读取 `AGENTS.md`、`periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md`、`rules/WORKSPACE.md`
- 保持文件职责边界清晰：
  - `rules/SOUL.md`：AI 身份与底层行为
  - `rules/USER.md`：用户画像与偏好
  - `rules/COMMUNICATION.md`：表达与沟通风格
  - `rules/WORKSPACE.md`：目录路由与文件归档
  - `rules/skills/`：可复用工作流与方法

晋升门槛：
- 跨项目可复用
- 已被多次验证或至少高度稳定
- 对未来决策有明确价值

禁止事项：
- 不要把一次性项目细节误晋升成长期规则
- 不要修改无关文件
- 不要把沟通风格规则写进技术工作流文件
- 不要为了“看起来做了很多”而过度改写

对 `{{OBSERVATIONS_PATH}}` 的处理：
- 保留仍有中短期价值的 `🟡` 项
- 删除已晋升到 rules 的内容
- 删除明显过期、无复用价值的 `🟢` 噪音
- 保持文件整体可读，不要把历史全部抹平

收尾：
- 更新必要的 `rules/` 文件
- 重写 `{{OBSERVATIONS_PATH}}`
- 更新 `C:/Users/Administrator/.codex/automations/ai-heartbeat-reflector/memory.md`
- 最后用中文给出一个简短 promotion summary：晋升了什么、清理了什么、还有什么保留在 `OBSERVATIONS.md`
