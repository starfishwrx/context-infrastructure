# Hermes 国产 API 调研来源索引

调研时间：2026-07-17。下列摘录来自检索结果中的原始页面摘要，关键配置应以现场安装版本的 `hermes model` 和对应厂商控制台为准。

## Tier 1：Hermes 官方资料

### Hermes CLI 命令参考

[NousResearch/hermes-agent CLI commands](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md)

> Force a provider: ... zai, kimi-coding, kimi-coding-cn, minimax, minimax-cn, ... alibaba, alibaba-coding-plan, deepseek, ... qwen-oauth, ... stepfun, tencent-tokenhub ...

> To add another provider ... exit your session and run hermes model from the terminal.

> /model custom:qwen-2.5 ... /model custom:local:qwen-2.5

用途：验证 Hermes 有国产原生 provider，并支持 custom endpoint。`hermes model` 是增加 provider 的入口；会话内 `/model` 主要用于切换已经配置的模型。

### Hermes 环境变量参考

[NousResearch/hermes-agent environment variables](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/reference/environment-variables.md)

> Custom DashScope base URL (default: https://dashscope-intl.aliyuncs.com/compatible-mode/v1; use https://dashscope.aliyuncs.com/compatible-mode/v1 for mainland-China region)

用途：验证 DashScope 中国大陆与国际 endpoint 不同。

### Hermes 配置与诊断入口

[Hermes Agent bundled skill documentation](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent.md)

> hermes config path ... hermes config env-path ... hermes config check ... hermes doctor [--fix] ... hermes status [--all]

> context_length ... clear to "" for auto-detect from server /v1/models

用途：验证配置文件定位、诊断命令和 `/v1/models` 自动探测边界。

## Tier 1：国产模型厂商资料

### DeepSeek 已提供 Hermes 专门集成页

[DeepSeek: Integrate with Hermes Agent](https://api-docs.deepseek.com/quick_start/agent_integrations/hermes/)

> This agent is provided entirely by a third party ... We cannot guarantee its effectiveness or security ...

用途：DeepSeek 官方承认 Hermes 集成路径，但同时明确 Hermes 是第三方项目，最终兼容性和安全性仍由使用者验证。

[DeepSeek API first call](https://api-docs.deepseek.com/guides/agent_integrations/opencode)

> The DeepSeek API uses an API format compatible with OpenAI/Anthropic.

> base_url="https://api.deepseek.com"

用途：验证 DeepSeek 的 OpenAI-compatible 入口。

[DeepSeek thinking mode and tool calls](https://api-docs.deepseek.com/guides/thinking_mode/)

页面提供 `tools` 定义与 thinking mode 示例。用途：验证工具调用属于必须单独测试的协议层，不应只测普通文本聊天。

### 阿里云需要区分三套 URL 与对应 Key/套餐

[Alibaba Cloud Model Studio base URL](https://help.aliyun.com/en/model-studio/base-url)

> A Base URL must be used together with an API Key from the same billing plan; otherwise, a 401 error occurs. API Keys are independent across regions ...

用途：验证中国区/国际区、套餐类型和 Key 必须匹配。

[Alibaba Cloud Coding Plan](https://help.aliyun.com/en/model-studio/coding-plan)

> OpenAI-compatible protocol: https://coding.dashscope.aliyuncs.com/v1

用途：验证 Coding Plan 使用专用 endpoint，不能照搬普通 Model Studio 地址。

[Alibaba Cloud: integrate third-party models with Hermes Agent](https://help.aliyun.com/en/simple-application-server/use-cases/hermes-agent-third-party-model)

页面给出 Bailian Token Plan、MiniMax、火山方舟和腾讯 Token Plan 的 Hermes 配置示例。用途：确认国产厂商侧已有 Hermes 部署文档，但具体配置需按购买的套餐版本读取。

[Alibaba Cloud private network access](https://help.aliyun.com/en/model-studio/access-model-studio-through-privatelink)

页面提供通过 PrivateLink 调用 Model Studio 的方法。用途：说明完全无公网环境需要企业私网 endpoint 或本地模型，单靠 U 盘无法让云 API 可达。

## Tier 3-4：独立/行为证据覆盖情况

本轮定向搜索没有找到足以支撑“所有国产 OpenAI-compatible API 都能无修改运行”的高质量 Hermes issue 或 production post-mortem。公开证据主要来自 Hermes 与厂商官方文档。因此报告只确认官方支持入口，不把普通聊天成功等同于 Agent 工具调用已通过。

