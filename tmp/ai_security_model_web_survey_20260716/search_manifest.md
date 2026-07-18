# 内置网页搜索重跑：Search Manifest

## 目标

验证 AgentKey 上一版是否存在时效性偏差，并重新调研 2025-07-16 至 2026-07-16 的模型、逆向代理和 prompt-injection 前沿。

## 产出

| 文件 | 路径 |
|---|---|
| 最新前沿报告 | `contexts/survey_sessions/ai_models_reverse_engineering_security_web_search_survey_20260716.md` |
| AgentKey 上一版 | `contexts/survey_sessions/ai_models_reverse_engineering_security_survey_20260716.md` |

## 并行证据线

| Agent | 范围 | 状态 |
|---|---|---|
| `web_latest_models` | 最新模型、官方 agent、Trusted Cyber Access、开放权重模型 | completed |
| `web_latest_jailbreak` | 2025-2026 jailbreak、间接注入、信息流与授权防御 | completed |
| `web_latest_reverse` | 最新逆向 benchmark、论文和 MCP 工具生态 | completed |

## 核心新增来源

- xAI Grok 4.5 与 Grok Build
- OpenAI GPT-5.6、Trusted Access、GPT-5.5-Cyber
- Anthropic Fable 5 / Mythos 5
- RARE、REFORGE、AutoDecompiler、CrackMeBench、FORGE
- IPI Arena、ChatInject、ARGUS、FIDES
- BinaryAudit、Ghidra/radare2/IDA/Binary Ninja/JADX MCP

## 边界

- 不使用 AgentKey。
- 技术事实优先使用一手来源。
- X 帖子仅作发现线索。
- 不保存可复制的 jailbreak payload 或未授权攻击步骤。
