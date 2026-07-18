# Search Manifest

## 产出文件索引

| 文件 | 路径 | 说明 |
|---|---|---|
| Scratchpad | `tmp/ai_security_model_survey_20260716/scratchpad.md` | Claim 与研究边界 |
| Search Manifest | `tmp/ai_security_model_survey_20260716/search_manifest.md` | 调用与证据索引 |
| AgentKey MCP Bridge | `tmp/ai_security_model_survey_20260716/agentkey_mcp_call.ps1` | 通过标准 MCP 协议调用已配置的 AgentKey |
| 最终报告 | `contexts/survey_sessions/ai_models_reverse_engineering_security_survey_20260716.md` | 中文内部调研报告 |

## 工具状态

- AgentKey MCP 配置有效，initialize 返回 HTTP 200。
- Codex 0.144.1 当前任务未把 AgentKey tools 映射为原生工具。
- 回退方式：通过标准 MCP JSON-RPC 调用 AgentKey 的工具发现与执行端点。

## Subagent 原始产出

| Agent | 工件 | AgentKey 调用 | 状态 |
|---|---|---:|---|
| `models_routes` | `tier_models_routes.md` | 2 Brave + 1 Twitter，2.2 credits | completed |
| `prompt_bypass_research` | `tier_prompt_bypass.md` | 2 Brave + 1 Twitter，2.2 credits | completed |
| `reverse_agents` | `tier_reverse_agents.md` | 3 Brave + 1 Twitter，2.8 credits | completed |

## 数据覆盖与限制

- 成功检索共 10 次，按端点单价估算 7.2 credits；另有一次参数错误的失败尝试，实际账单以 AgentKey 账户记录为准。
- X/Twitter 三次检索中，两次返回 0 条；仅证据线 A 获得相关帖子。
- 主要结论以论文、GitHub 仓库、benchmark 和模型卡为依据。
- Grok 缺少与 Gemini、Claude、Codex 在授权逆向任务上的可靠同场 benchmark。
- 未收录具体 jailbreak payload、恶意代码或未授权攻击步骤。
