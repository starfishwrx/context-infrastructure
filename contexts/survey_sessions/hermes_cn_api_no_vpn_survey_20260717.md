# Hermes Agent 搭配国产 API 与无 VPN 现场修复指南

调研日期：2026-07-17  
适用对象：NousResearch/hermes-agent。现场仍需用仓库 URL 或 `hermes --version` 校准项目身份。

## 无 VPN 可直连国产 API，现场风险集中在地址、套餐与工具调用

Hermes 已原生支持多家国产模型提供商，也支持自定义 OpenAI-compatible endpoint。无 VPN 且具备正常中国大陆互联网时，DeepSeek、DashScope 等国内 API 可以直接使用。现场真正的高频故障是区域、套餐、Base URL、模型 ID、代理变量和工具调用兼容性错配。

U 盘值得带，但用途是版本匹配的离线救援包。只拷源码不足以完成离线安装。若现场完全没有公网，任何云模型 API 都不可达，需要企业私网 endpoint 或本地 OpenAI-compatible 模型服务。

快速跳转：

1. [国产 API 选择与地址](#国产-api-优先走原生-provider阿里云要区分三套地址)
2. [Hermes 配置步骤](#通过-hermes-model-配置provider会话内-model-只负责切换)
3. [无 VPN 处理](#无-vpn-要拆成三种网络条件处理)
4. [U 盘准备](#u-盘应带可回滚救援包而不是孤立源码)
5. [现场排障顺序](#现场按网络鉴权协议hermes-四层排查)

## 国产 API 优先走原生 provider，阿里云要区分三套地址

Hermes 的[官方 CLI 文档](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md)列出了 `deepseek`、`zai`、`kimi-coding`、`kimi-coding-cn`、`minimax`、`minimax-cn`、`alibaba`、`alibaba-coding-plan`、`qwen-oauth`、`stepfun`、`tencent-tokenhub` 等 provider。原生 provider 会处理部分厂商差异，优先级高于手写 custom 配置。

| 厂商/方案 | Hermes 入口 | 现场判断 |
|---|---|---|
| DeepSeek | `deepseek` | DeepSeek 已有[官方 Hermes 集成页](https://api-docs.deepseek.com/quick_start/agent_integrations/hermes/)，OpenAI-compatible Base URL 为 `https://api.deepseek.com` |
| 阿里云普通按量 API，中国大陆 | `alibaba` 或 custom | 使用 `https://dashscope.aliyuncs.com/compatible-mode/v1`，Key 必须属于相同区域和套餐 |
| 阿里云 Coding Plan | `alibaba-coding-plan` | 使用专用地址 `https://coding.dashscope.aliyuncs.com/v1`，不要与普通按量 API 地址混用 |
| 阿里云国际区 | `alibaba` 或 custom | 使用 `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`，国际区 Key 与大陆 Key 分离 |
| 智谱 GLM | `zai` | 通过 provider wizard 读取当前模型和凭证要求，不手抄旧教程 URL |
| Kimi | `kimi-coding-cn` | 中国大陆优先选 `-cn` provider；模型名以账户控制台为准 |
| MiniMax | `minimax-cn` | 中国大陆优先选 `-cn` provider；Coding Plan 与普通 API 的凭证可能不同 |
| 阶跃星辰 | `stepfun` | 使用原生 provider，现场确认模型是否支持 tools |
| 腾讯 Token Plan | `tencent-tokenhub` | 使用原生 provider和对应套餐凭证 |
| 火山方舟、硅基流动、企业网关 | custom | 使用控制台提供的 OpenAI-compatible URL 和模型/endpoint ID，必须单测 tools 与 streaming |

阿里云的[Base URL 文档](https://help.aliyun.com/en/model-studio/base-url)明确说明：Base URL 与 API Key 必须来自相同计费计划和区域，否则会出现 401。其[Coding Plan 文档](https://help.aliyun.com/en/model-studio/coding-plan)给出的协议地址是 `https://coding.dashscope.aliyuncs.com/v1`。这意味着网上常见的 DashScope 配置教程不能跨套餐照抄。

模型名也不能凭产品宣传名猜测。火山方舟等平台有时要求 endpoint ID，其他平台要求具体模型 ID。以甲方控制台中可调用的 ID 为准。

## 通过 `hermes model` 配置 provider，会话内 `/model` 只负责切换

### 1. 先确认当前安装和配置位置

在 Hermes 会话外运行：

```powershell
Get-Command hermes -ErrorAction SilentlyContinue
hermes --version
hermes config path
hermes config env-path
hermes config
hermes config check
hermes status --all
hermes doctor
```

先复制 `config.yaml`、`.env`、启动脚本、Docker Compose 或系统服务定义。`hermes doctor --fix` 会修改状态，完成备份后再考虑运行。

### 2. 新增国产 provider

退出正在运行的 Hermes 会话，然后运行：

```powershell
hermes model
```

选择原生 provider，输入甲方自己的 API Key 和准确模型名。官方文档说明，`hermes model` 可以添加 provider、完成认证和保存 endpoint；会话内 `/model` 用于切换已经配置的模型，无法完整替代首次配置。

配置完成后：

```powershell
hermes config check
hermes doctor
hermes status --all
hermes
```

### 3. 厂商没有原生 provider 时使用 custom

仍从 `hermes model` 进入 custom/OpenAI-compatible 配置，填写：

1. Base URL，通常截止到 `/v1`，不要再手工拼 `/chat/completions`。
2. API Key。
3. 厂商控制台显示的模型 ID 或 endpoint ID。
4. `context_length`。只有接口可靠实现 `/v1/models` 时才适合自动探测。

配置过 custom endpoint 后，会话内可以使用官方文档给出的形式切换：

```text
/model custom:模型名
/model custom:自定义提供商名:模型名
```

具体 provider 名和 config 层级可能随 Hermes 版本变化。现场以 `hermes model` 生成的配置为准，避免直接复制网上某个旧版 `config.yaml`。

## 无 VPN 要拆成三种网络条件处理

| 现场条件 | 可行方案 | 关键限制 |
|---|---|---|
| 无 VPN，有国内公网 | 直接使用国内 provider 和中国区 endpoint | GitHub/PyPI 可能慢或不可达，但模型推理可独立正常 |
| 无 GitHub，国内 API 可达 | 保留现有 Hermes，只修改 provider；更新包和依赖通过 U 盘带入 | 不要为了 API 配置问题先重装 |
| 完全无公网 | 使用企业 PrivateLink/内网网关，或本地 LM Studio、Ollama、vLLM 等 OpenAI-compatible 服务 | 云 API 与联网工具都无法工作 |

### 无 VPN但有国内公网

DeepSeek、阿里云中国区、Kimi 中国区等服务设计为国内访问，不需要 VPN。全局 VPN 或残留代理反而可能把流量送到境外出口，造成区域判断、延迟或 TLS 问题。现场同时检查进程代理与 WinHTTP 代理：

```powershell
Get-ChildItem Env: | Where-Object Name -Match 'PROXY|SSL_CERT'
netsh winhttp show proxy
Resolve-DnsName api.deepseek.com
Test-NetConnection api.deepseek.com -Port 443
```

发现 `HTTP_PROXY`、`HTTPS_PROXY`、`ALL_PROXY` 时，先记录原值，再在当前测试进程中临时清除并做 A/B 测试。不要直接删除系统级代理配置。

### 无 GitHub但国内 API 可达

这是最可能的现场情况。Hermes 已安装时，只需修正 API 配置和重启对应进程。安装或更新才依赖 GitHub、Python 包源和 uv 下载链路。优先修复现有版本，避免引入版本迁移。

更新确有必要时，使用提前准备并验证过的 Git bundle、准确版本源码和依赖缓存。随机 GitHub 加速站会引入供应链风险，不建议在客户机器使用。

### 完全无公网或仅企业内网

U 盘只能传输程序，不能替代网络。云模型调用需要以下任一通道：

1. 企业批准的公网出口。
2. 云厂商 PrivateLink 或企业内部 API 网关。阿里云提供了[Model Studio PrivateLink 方案](https://help.aliyun.com/en/model-studio/access-model-studio-through-privatelink)。
3. 现场本地模型服务。Hermes 官方 provider 列表包含 `lmstudio`，其他本地服务可走 custom OpenAI-compatible endpoint。

本地模型还要验证工具调用能力。低参数量聊天模型即使能回答文本，也可能无法可靠地产生结构化 `tool_calls`。

## U 盘应带可回滚救援包，而不是孤立源码

建议目录：

```text
hermes-rescue/
  00-docs/
  01-hermes-exact-version/
  02-runtime-installers/
  03-dependency-cache/
  04-diagnostics/api_probe.ps1
  05-backups/
  06-change-log-template/
```

内容要求：

1. 甲方当前版本对应的源码 ZIP 和 Git bundle。额外带 latest 版本，但不要默认升级。
2. Hermes CLI、环境变量、Windows/Linux 安装文档的离线副本。
3. 与现场 OS、CPU 架构匹配的 Git、Python、uv 安装包。
4. 在同 OS、同架构、同 Python 版本上实际验证过的依赖缓存。只下载源码无法覆盖编译型依赖。
5. 本调研附带的 `api_probe.ps1`，用于独立测试 `/models`、普通 chat 和 tool calling。
6. 空白配置备份目录与变更记录模板。

不要把客户 API Key 放入 U 盘，也不要把 Key 写进命令行历史。修复完成后由客户决定是否轮换暴露过的凭证。Windows Defender 若拦截 Hermes 自带的 `uv.exe`，先核对来源和哈希，再由客户批准放行；不要关闭杀毒软件。

## 现场按网络、鉴权、协议、Hermes 四层排查

### 第一层：网络和 TLS

```powershell
Resolve-DnsName <API域名>
Test-NetConnection <API域名> -Port 443
curl.exe -I https://<API域名>
```

如果返回公司登录页、WAF HTML 或证书链错误，问题在 Hermes 之外。检查代理、企业 CA、DNS 和出口白名单。

### 第二层：绕过 Hermes 测 API

运行本次生成的探针：

```powershell
powershell -ExecutionPolicy Bypass -File .\api_probe.ps1 `
  -BaseUrl 'https://api.deepseek.com' `
  -Model '<甲方控制台中的模型ID>'
```

脚本会遮罩输入 API Key，并依次测试 `/models`、普通 chat 和 tools。某些兼容接口没有 `/models`；该项失败时继续使用手工模型名测试 chat。

### 第三层：按错误类别定位

| 症状 | 首要检查 |
|---|---|
| 401 | Key 与区域/套餐不匹配；服务进程没有加载 `.env`；Key 有空格 |
| 403 | IP 白名单、账户权限、区域限制、企业出口策略 |
| 404 | Base URL 重复 `/v1`；误填完整 `/chat/completions`；模型/endpoint ID 错误 |
| 400 | tools、JSON Schema、thinking/reasoning 参数或消息角色不兼容 |
| 429 | 余额、RPM/TPM、并发和 Coding Plan 配额 |
| 超时 | 代理、DNS、TLS 检查、流式连接被网关截断 |
| 普通 chat 成功但无 `tool_calls` | 模型或兼容层不具备 Agent 所需工具调用能力 |
| 命令行成功，gateway 失败 | gateway 服务加载了另一份 `.env`，或修改后尚未重启 |

### 第四层：回到 Hermes 验收

验收顺序：

1. `hermes config check` 无缺失项。
2. `hermes doctor` 没有阻断问题。
3. CLI 完成一次普通对话。
4. CLI 完成一次真实工具调用，例如读取客户允许的测试目录。
5. 如有 Telegram、Discord 或 Web gateway，再重启该服务并重复测试。
6. 保存修改前后配置差异，API Key 打码；保留回滚包。

## 证据边界与今晚最有价值的动作

官方证据确认了 Hermes 的国产 provider 和厂商集成入口，但本轮未找到足量 production issue 来证明每个国产模型、每个套餐和每个 Hermes 版本都能完整支持 tools/streaming。最终兼容性必须以甲方实际环境验收。

今晚最有价值的动作是向甲方索取：仓库 URL、`hermes --version`、操作系统、完整错误日志、provider、Base URL、模型 ID、安装方式和现场网络限制。拿到这些后，才能准备准确版本和平台匹配的离线依赖包。

## 完整证据与现场探针已留存在调研工件中

- Claim 与验证状态：`tmp/hermes_cn_api_20260717/scratchpad.md`
- 来源原文索引：`tmp/hermes_cn_api_20260717/source_index.md`
- 检索覆盖与证据缺口：`tmp/hermes_cn_api_20260717/search_manifest.md`
- PowerShell API 探针：`tmp/hermes_cn_api_20260717/api_probe.ps1`
