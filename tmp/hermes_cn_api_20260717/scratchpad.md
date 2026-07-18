# Hermes Agent 搭配国产 API 调研草稿

调研日期：2026-07-17

## 本轮要回答的决策

1. NousResearch/hermes-agent 是否原生支持常见国产模型提供商。
2. 原生 provider 与 OpenAI-compatible custom endpoint 分别怎样配置。
3. 没有 VPN 时，哪些操作仍可完成，哪些依赖需要提前离线准备。
4. 现场故障应如何区分网络、鉴权、模型名、协议兼容和 Hermes 配置问题。

## Claim Extraction

| Claim | 来源层级 | 验证通道 | 验证状态 |
|---|---|---|---|
| Hermes 支持 DeepSeek、Qwen/Alibaba、Kimi、GLM 等国产提供商 | Tier 1 官方文档 | provider 注册表、CLI 文档、相关 issue | 待验证 |
| 任意 OpenAI-compatible API 填 base URL 和 model 即可工作 | Tier 1 官方叙事 | custom provider 实现、/v1/models 行为、工具调用 issue | 待验证 |
| 无 VPN 不影响国产 API 推理 | 厂商网络假设 | 中国大陆官方 endpoint、DNS/连通性测试 | 待验证 |
| 把源码拷到 U 盘即可完成离线修复 | 现场经验假设 | 安装脚本、依赖管理、版本与平台约束 | 待验证 |
| 普通聊天成功代表 Agent 可正常工作 | 常见误判 | tool calling、streaming、JSON schema 兼容证据 | 待验证 |

## 验证结果

| Claim | 结论 | 依据与边界 |
|---|---|---|
| Hermes 支持多家国产 provider | 已验证 | 官方 CLI 列出 `deepseek`、`zai`、`kimi-coding-cn`、`minimax-cn`、`alibaba`、`qwen-oauth`、`stepfun`、`tencent-tokenhub` 等 |
| 任意兼容接口填 URL 即可工作 | 部分成立 | Hermes 支持 custom endpoint；`/v1/models`、tools、streaming、reasoning 字段仍可能不完整 |
| 无 VPN 不影响国产 API 推理 | 条件成立 | 国内 endpoint 可直连；Key、区域、套餐、代理变量必须匹配。完全断网时云 API 仍不可用 |
| 只带源码即可离线修复 | 不成立 | 还需要准确版本、Python/uv 运行时、平台匹配依赖缓存、配置备份和 API 探针 |
| 普通聊天成功代表 Agent 正常 | 不成立 | Agent 还依赖结构化 tool calls、流式响应、上下文和错误重试 |

## 初步风险假设

- 项目名称仍需以现场仓库 URL 或 `hermes --version` 校准。
- 同为国产模型，不同厂商对 OpenAI 协议、工具调用和模型 ID 的兼容程度不同。
- 无 VPN、无 GitHub、完全无公网是三种不同约束，处理方式不同。

## 核心机制判断

1. 模型 API 可达性和 Hermes 安装/更新可达性是两条链路。国内模型 API 可直连，不代表 GitHub/PyPI 可用。
2. 国产 API 最常见的配置事故来自区域、套餐和 endpoint 混用。阿里云尤为明显：大陆普通兼容接口、国际接口、Coding Plan 专用接口不是同一个地址。
3. 现场验收至少分三层：TCP/TLS 与鉴权、普通 chat completion、tools/streaming 的 Agent 协议。
4. 公开 Tier 4 故障证据不足，最终结论需要以甲方的 Hermes 版本、provider、模型和日志校准。
