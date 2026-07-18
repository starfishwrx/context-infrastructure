# Hermes 国产 API 调研 Search Manifest

## 产出文件索引

| 文件 | 路径 | 说明 |
|---|---|---|
| Scratchpad | `tmp/hermes_cn_api_20260717/scratchpad.md` | Claim 与判断过程 |
| Search Manifest | `tmp/hermes_cn_api_20260717/search_manifest.md` | 检索范围、来源及回退说明 |
| Source Index | `tmp/hermes_cn_api_20260717/source_index.md` | 关键来源与原文摘录 |
| 最终报告 | `contexts/survey_sessions/hermes_cn_api_no_vpn_survey_20260717.md` | 配置教程与现场处置方案 |

## Subagent 使用情况

本次用户要求使用本地调研技能，但未明确要求 Multi-Agent、并行调研或 subagent。按 `workflow_deep_research_survey.md` 的 Codex Studio 分流规则，由主线程执行调研；未启动 subagent。

## 检索计划

1. Tier 1：Hermes 官方 README、CLI、环境变量、provider 配置和安装文档。
2. Tier 1：国产模型厂商的 OpenAI-compatible endpoint 与网络区域说明。
3. Tier 3-4：Hermes GitHub issues、代码注册表、失败症状与兼容边界。
4. 交叉验证：区分无 VPN、无法访问 GitHub、完全断网。

## 实际检索覆盖

- Hermes 官方 CLI、环境变量、配置与诊断文档。
- DeepSeek 官方 Hermes 集成、OpenAI-compatible 和 tool calling 文档。
- 阿里云 Model Studio 区域 URL、Coding Plan、Hermes 第三方模型配置、PrivateLink 文档。
- Hermes GitHub issues 定向搜索。相关 production issue 样本不足，已在报告中降低结论强度。

## 证据缺口

- 尚未拿到甲方的 Hermes 版本、操作系统、provider、模型名和错误日志。
- Kimi、GLM、MiniMax、火山方舟等具体 endpoint 会随套餐与版本变化，本报告优先建议走 Hermes 原生 provider wizard，并以甲方控制台显示的 endpoint 为准。
- 无现场网络环境，无法替甲方验证 DNS、代理、IP 白名单和账户权限。
