# AI 模型用于授权逆向工程：2026 最新前沿版与搜索工具对比

调研日期：2026-07-16  
时间窗口：优先 2025-07-16 至 2026-07-16，重点覆盖 2026 年 4 至 7 月  
检索方式：Codex 内置网页搜索，不使用 AgentKey  
来源优先级：官方模型文档、厂商公告、arXiv/OpenReview、作者 GitHub、活跃项目仓库

## 核心结论

上一版确实偏旧。AgentKey 找到的机制性结论大体成立，但它漏掉了过去三个月内改变判断的一批重要发布：

1. Grok 4.5 已于 2026-07-08 正式发布，并明确面向 coding 和 agentic tasks。
2. OpenAI 与 Anthropic 已经推出身份验证型高权限 cyber 路线。它们通过账户、用途和部署层开放授权逆向能力，而不是依赖越狱提示。
3. 2026 年 4 至 7 月出现了新一代逆向 benchmark 与代理系统：RARE、REFORGE、AutoDecompiler、CrackMeBench、FORGE、REBench、BinDeObfBench。
4. 逆向工具生态从早期单一 Ghidra 插件发展为 Ghidra、IDA、Binary Ninja、radare2、JADX 的 MCP 工具层，并开始支持多 agent、动态反馈和证据链。
5. 最新 prompt-injection 研究的重点已从固定 DAN/JSON 提示，转向 chat-template 混淆、工具描述投毒、上下文授权、provenance 和信息流控制。

最重要的新判断是：

> 对合规的专业安全团队，经过身份和用途验证的 cyber 专用访问，是当前最可审计、最容易明确责任边界的低误拒候选路线。它的实际逆向能力、误拒率和相对优势仍需要在统一内部 benchmark 上验证。

## 当前模型版图已经变化

### Grok 4.5 确实存在，而且刚刚发布

xAI 于 2026-07-08 发布 [Grok 4.5](https://x.ai/news/grok-4-5)，定位为 coding、agentic tasks 和 knowledge work。其 [API 文档](https://docs.x.ai/developers/grok-4-5)确认模型 ID 为 `grok-4.5`，支持 reasoning、function calling、结构化输出、Web/X 搜索和代码执行。

xAI 同时在 2026 年 5 月发布 [Grok Build](https://x.ai/news/grok-build-cli)。截至 2026-07-09 的 [Grok Build changelog](https://x.ai/build/changelog)显示，它已经支持：

- MCP、skills、plugins 和 hooks。
- 并行 subagents 与 worktree。
- 长任务 goal mode。
- Web/X 搜索。
- Windows、Linux、macOS 和 IDE/ACP 接入。
- 权限模式、后台任务、会话恢复与上下文压缩。

xAI 官方新闻索引还确认，用户可以把 Grok 订阅用于 OpenCode。由此看，用户提出的第二条路线已经从社区拼装方案变为厂商正式支持的产品路径。

但这里必须区分两个问题：

- Grok 4.5 是强 coding/agent 模型，这有官方 benchmark 支持。
- Grok 4.5 是否是最好的二进制逆向模型，目前没有专门 benchmark 证据。

### Gemini 2.5 已经不是 Google 当前前沿

Google 当前 [Gemini API 模型目录](https://ai.google.dev/gemini-api/docs/models)更新于 2026-07-09，模型版图已进入 Gemini 3 系列。Gemini 3.5 Flash 被定位为面向持续 agentic 和 coding 任务的稳定模型，Gemini 3.1 Pro 继续承担复杂推理和 agent 编程。

因此，如果今天重新做模型选型，继续把 Gemini 2.5 当成唯一代表会产生明显时间偏差。2.5 仍可用，但不再代表 Google 当前前沿能力。

### OpenAI 当前路线已经进入 GPT-5.6 与专用 Cyber Access

OpenAI 于 2026-07-09发布 [GPT-5.6](https://openai.com/index/gpt-5-6/)。官方称 Sol 是其当前最强 coding 和 cybersecurity 模型，支持 programmatic tool calling、多 agent 与长时任务。

更值得关注的是 [Trusted Access for Cyber](https://help.openai.com/en/articles/20001258-trusted-access-for-cyber/)：

- 明确允许在授权环境中用于 malware analysis、binary reverse engineering、red teaming、penetration testing 和 exploit validation。
- 标准 GPT-5.5、Trusted Access 与 GPT-5.5-Cyber 形成分级访问。
- GPT-5.5-Cyber 更偏向专门授权工作流，配套身份验证、账户安全、用途审核和监控。
- 官方明确说明它不会移除所有 safeguards，也不允许超出授权目标。

[GPT-5.5-Cyber 发布说明](https://openai.com/index/gpt-5-5-with-trusted-access-for-cyber/)进一步说明：它的初期目标主要是降低合法安全研究的误拒，而不是把基础模型变成能力更强的新模型。

这恰好验证了上一版的一个正确判断：更少拒答和更强能力是两个不同变量。区别是，2026 年已经出现官方治理路径来处理拒答变量。

### Anthropic 已经提供同底模、不同 Cyber Safeguard 的双版本

Anthropic 于 2026 年发布 [Claude Fable 5 与 Mythos 5](https://www.anthropic.com/news/claude-fable-5-mythos-5)：

- Fable 5 面向公开使用，部署更强的 cyber classifiers。
- Mythos 5 与 Fable 5 使用同一模型，但为获批安全合作伙伴放宽或移除特定 cyber safeguards/classifiers；其他账户、使用政策、监控和访问控制仍以官方条款为准。
- Anthropic 报告，外部红队尚未找到能在长时 agent 任务中稳定关闭 Fable 5 safeguards 的 universal jailbreak。
- Mythos 5 通过 trusted access 提供，而不是通过公开提示词解锁。

这使“去除道德限制”出现了一个更准确的工程表达：

> 同一个高能力模型可以通过访问层、账户层和用途验证提供不同的安全行为，而不必公开一个永久越狱入口。这证明了治理机制的可行性，并不单独证明该版本在逆向任务上更强。

## 目前存在的六条路线

| 路线 | 2026 状态 | 主要价值 | 主要限制 |
|---|---|---|---|
| 本地开放权重基础模型 | 成熟 | 数据隐私、版本固定、可微调 | 能力和工具稳定性可能弱于前沿模型 |
| Abliterated/Heretic 模型 | 活跃迭代 | 降低拒答，可控制 chat template | 作者自测多，命名不能证明能力 |
| 前沿托管模型 + OpenCode/CLI Agent | 快速成熟 | 强推理、长上下文、工具生态 | 数据边界、服务端策略和成本 |
| Trusted Cyber Access | 2026 年关键新增 | 合法降低误拒，保留治理与审计 | 需要身份、用途和组织审核 |
| 领域微调 + 执行反馈 | 研究快速推进 | 直接提高反编译语义正确率 | 数据与评测成本高，仍需独立复现 |
| 固定 Prompt/JSON/Jailbreak | 持续存在但地位下降 | 低成本红队测试 | 脆弱、版本相关、不能解决能力和工具安全 |

## 开放权重与去对齐模型的最新情况

### 最新基础模型已经转向 agentic coding

[Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next)于 2026-02 发布，80B 总参数、3B active、256K 原生上下文，官方直接面向 coding agents、工具调用和从执行失败中恢复。

社区很快产生 [Huihui-Qwen3-Coder-Next-abliterated](https://huggingface.co/huihui-ai/Huihui-Qwen3-Coder-Next-abliterated)，并针对 llama-server tool calling 和 OpenCode 调整 chat template。这说明最新去对齐路线已经开始和 agent harness 深度绑定，而不是只做聊天模型。

### Heretic 已经取代早期手工 abliteration，成为自动搜索工具

[Heretic](https://github.com/p-e-w/heretic)在 2026-05 发布 v1.3.0，支持 Qwen3.5、Gemma 4、集成 benchmark 和可复现运行。较新的变体采用不同的权重方向搜索和 magnitude-preserving 方法，以降低 KL divergence。

但最新模型卡也暴露出三个问题：

1. 模型名称包含 uncensored/heretic，不代表拒答已真正消失。
2. KL divergence 很低，不代表反编译正确率高。
3. 大多数 benchmark 仍由模型发布者自己运行。

[UGI Leaderboard](https://huggingface.co/spaces/DontPlanToEnd/UGI-Leaderboard)仍然值得用来测 willingness 和敏感主题知识，但不能当作逆向工程能力排行榜。

### Cyber 定向社区模型非常新，但证据质量参差

2026 年 Hugging Face 上出现了大量基于 Qwen3.6、Gemma 4 等基础模型的 cyber 或 Heretic 变体。例如 [Qwen3.6-27B-Uncensored-Cyber](https://huggingface.co/philbert440/Qwen3.6-27B-Uncensored-Cyber)与 [Dolphin3-Cyber-8B-GGUF](https://huggingface.co/RavichandranJ/Dolphin3-Cyber-8B-GGUF)的模型卡声称针对 malware、vulnerability 和 offensive-security prompt 优化拒答方向。这些声明主要来自发布者自述。

这些模型适合作为候选集，不适合直接进入生产。至少需要重新测试：

- 函数命名和行为摘要。
- 数据流、类型和结构体恢复。
- 协议字段推断。
- 幻觉率。
- 工具调用格式。
- 样本内 prompt injection。

## 2026 年逆向工程研究的真正新方向

### RARE：二进制会反向控制 Agent

2026-07-14 的 [When Binaries Talk Back](https://arxiv.org/abs/2607.12507)是本轮最关键的新论文。

它研究的不是如何让模型逆向二进制，而是二进制如何通过字符串、反编译输出和工具报告影响模型：

- 没有运行时控制时，模型在 35/40 个对抗样本上提出了被植入的不安全动作。
- 仅把二进制内容显示为 data 后，仍出现 15 次不安全提议。
- Tool Authorization 阻止了这 15 次动作。
- Provenance Gate 阻止来自同一来源的多个工具视图被错误计算成独立证据。

这直接推翻了“只要在 System Prompt 中告诉模型不要听样本里的指令就安全”的思路。语言层提示不足以构成权限边界。

### AutoDecompiler：从一次生成变成执行反馈循环

[AutoDecompiler](https://arxiv.org/abs/2606.16162)于 2026-06-15 发布。它使用编译、执行和输入输出测试反馈进行多轮修正。

这条路线解决的是生成代码看起来合理、甚至可以编译，但行为与原二进制不一致的问题。论文报告，同规模、同输入设置下，反馈驱动模型在 behavioral re-executability 上持续优于单轮版本。

与去对齐相比，这更直接地改善了反编译任务的核心指标。

### FORGE：多 Agent 动态探索真实固件

[FORGE](https://arxiv.org/abs/2604.15136)把分析建模为 reasoning-action-observation 循环，并用 Dynamic Forest of Agents 并行探索、限制单 agent 上下文。

作者在 3,457 个真实固件二进制上报告发现 1,274 个漏洞，precision 为 72.3%。这是作者自报结果，仍需独立复现，但它代表的架构方向很清楚：

- 动态拆分分析路径。
- 每条路径保留可回放证据。
- 工具观察驱动下一步，而不是让模型一次性猜完整程序。

### CrackMeBench：可执行 oracle 让模型排名开始有意义

[CrackMeBench](https://arxiv.org/abs/2605.10597)于 2026-05 发布，使用教育型、确定性 CrackMe 和可执行评分。

在生成任务上，作者报告 GPT-5.5、Claude Opus 4.7 和 Kimi K2 的 pass@3 分别为 92%、58% 和 42%。数据集只有 20 项，不能外推到真实恶意软件或大型固件，但它比自由文本解释更接近可复现能力测试。

### REFORGE：很多排行榜先被 ground truth 污染

[REFORGE](https://arxiv.org/abs/2607.07738)于 2026-07-07 发布。它指出，编译优化会显著降低 binary-to-source 高置信对齐样本的比例；未配对比较可能通过 survivorship bias 夸大模型性能变化。

因此，内部 benchmark 必须保存：

- 编译器和优化等级。
- DWARF/源码映射。
- 反编译器版本。
- 对齐置信度。
- 哪些样本因无法可靠对齐而被排除。

### BinaryAudit：当前没有证据证明 Grok 更适合逆向

[BinaryAudit](https://quesma.com/benchmarks/binaryaudit/)使用真实网络软件和人工植入的后门，要求模型操作 Ghidra/radare2、定位后门并避免在 clean binary 上误报。

其当前公开结果中：

- Gemini 3.1 Pro Preview 的二进制分析 pass rate 为 49%，false positive rate 为 17%。
- GPT-5.2-Codex-xhigh 的 pass rate 为 46%，false positive rate 为 0%。
- Grok 4 为 9%，Grok 4.1 Fast 为 7%。

这不是 Grok 4.5 的成绩，所以不能用来否定 4.5。但它说明“Grok 更敢回答”没有转化为旧版本上的逆向优势。Grok 4.5 仍需单独测试。

## 最新逆向工具生态

2026 年的趋势是 MCP 工具接口快速扩张：

- [13bm/GhidraMCP](https://github.com/13bm/GhidraMCP)：约 70 个工具，支持异步反编译、多实例和 TCP 认证。
- [bethington/ghidra-mcp](https://github.com/bethington/ghidra-mcp)：截至 2026-07-16，README 声称提供 200 多个工具，覆盖 P-code、调试器、数据流和批处理；同时意味着写入和脚本权限风险更高。工具数量会随版本变化。
- [radareorg/radare2-mcp](https://github.com/radareorg/radare2-mcp)：radare2 官方组织下的 MCP 服务。
- [Binary Ninja MCP](https://github.com/fosdickio/binary_ninja_mcp)：覆盖 HLIL/MLIL/LLIL、类型和调用关系。
- [JADX-AI-MCP](https://github.com/zinja-coder/jadx-ai-mcp)：面向 APK、Java、Smali 和 Manifest。
- [ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp)：项目仍重要，但 README 已说明 GUI MCP 路线将逐步弃用，转向 idalib-mcp。
- [Rikugan](https://github.com/buzzer-re/Rikugan)：继续活跃，支持 IDA/Binary Ninja 和多 provider，但作者仍将其标为 work in progress。

选择工具时不应该只看工具数量。更重要的是：

- 默认只读还是默认可写。
- 是否允许任意脚本执行。
- 是否支持路径、网络和目标 allowlist。
- 是否记录工具调用与来源。
- 是否能对 mutation、patch、debug 和上传动作单独审批。

## Prompt、JSON 和 System Injection 的最新判断

### JSON 文件本身仍然没有特殊权限

2025 年流行的 Policy Puppetry、XML/JSON policy document、assistant prefill 确实能在部分旧版本模型上诱导安全策略失效。但近 12 个月的新研究显示，真正重要的机制是：

- chat template 和角色标记。
- 虚构多轮历史。
- tool description 与 MCP metadata。
- 检索触发与 RAG 污染。
- 上下文中的授权信息。
- source 到高风险 sink 的因果链。

因此，JSON 是载体之一，不是解锁开关。

### ChatInject：更接近用户记忆中的方法

[ChatInject](https://arxiv.org/abs/2509.22830)利用模型学到的 chat template、角色边界和伪对话结构，让外部数据被误解为高优先级指令。

论文在 GPT-4o、Grok-3、Gemini 2.5 Pro 和多个开放模型上验证了跨模型迁移，但没有覆盖 Grok 4.5、GPT-5.6 或 Claude Fable 5。它证明机制存在，不证明某个固定模板长期有效。

### IPI Arena：所有前沿 Agent 都仍然会被间接注入

2026-03 的 [IPI Arena](https://arxiv.org/abs/2603.15714)汇总 464 名参与者、272,000 次攻击、13 个前沿模型和 41 个工具/编码/计算机操作场景。

所有模型均出现成功攻击。原始 attack success rate 从 Claude Opus 4.5 的 0.5% 到 Gemini 2.5 Pro 的 8.5%。能力和抗注入性相关性很弱。

这意味着“选能力更强或限制更低的模型”不会自动得到安全 Agent。

### 2026 年防御开始转向授权与 provenance

[ARGUS](https://arxiv.org/abs/2605.03378)使用 influence provenance graph 检查不可信上下文如何传播到决策。

[FIDES](https://github.com/microsoft/fides)和相关 [信息流控制研究](https://openreview.net/forum?id=2FkswFYju5)把 trusted/untrusted、confidentiality 和 integrity 标签沿工具调用传播，并在敏感工具执行前确定性拦截。

[OpenAI 关于抗 prompt injection 的工程说明](https://openai.com/index/designing-agents-to-resist-prompt-injection/)也将重点放在 source-sink 分析、沙箱、用户确认和能力约束，而不是寻找更强的防御提示词。

对逆向 Agent 来说，正确架构是：

1. 二进制、反编译文本、README、issue、工具描述全部属于不可信 source。
2. Shell、网络、写文件、上传、patch、调试执行属于高风险 sink。
3. 模型可以提出动作，但授权系统决定能否执行。
4. 多个工具对同一二进制的观察不能自动被视为多个独立证据。

## 当前最值得测试的组合

### 组合 A：官方 Trusted Cyber Access

- GPT-5.6 或 GPT-5.5 + Trusted Access。
- 需要时申请 GPT-5.5-Cyber。
- Codex/OpenCode 作为 harness。
- Ghidra/radare2/JADX MCP 只读工具。
- 独立 VM、默认断网、工具审批。

优势：前沿能力与合法低误拒兼得。  
限制：需要审核，数据保留与 ZDR 要单独确认。

### 组合 B：Anthropic Mythos 5

- 通过 trusted-access partner 路线申请。
- Claude Code 或自建 agent harness。
- 文件与网络 sandbox。
- 反编译内容 provenance 标记。

优势：为获批合作方放宽或移除特定 cyber safeguards/classifiers。  
限制：访问范围小，30 天 retention 等政策需要评估。

### 组合 C：Grok 4.5 + Grok Build/OpenCode

- 使用 Grok 4.5 的长上下文、代码和 agent 能力。
- 对 MCP 工具权限做白名单。
- 使用内部 benchmark，而不是依赖 xAI 的通用 coding benchmark。

优势：新、agent 产品化速度快、X/Web 工具方便。  
限制：目前没有专门二进制 benchmark，不能预设它优于 GPT/Claude/Gemini。

### 组合 D：本地 Qwen3-Coder-Next/Heretic 路线

- 基础模型与 abliterated 版本同时跑。
- 用相同工具、相同样本和相同预算比较。
- 本地处理完整敏感样本。
- 必要时只把结构化、脱敏证据发送给前沿模型。

优势：数据控制和版本可重复。  
限制：必须自己承担模型供应链、评测和工具安全。

## 建议的内部验证计划

不要先测试谁更容易越狱。先测试谁真正完成逆向任务。

准备 30 至 50 个授权样本，分别测：

1. 函数命名和行为摘要。
2. 类型、结构体与变量恢复。
3. 协议字段与状态机推断。
4. 漏洞候选与证据定位。
5. 动态观察与最终结论的一致性。
6. 整程序覆盖率和长任务恢复。
7. 二进制字符串/README/MCP metadata 中的 prompt injection。

指标：

- 可执行或行为等价正确率。
- 拒答率和误拒率。
- 幻觉率。
- 后门发现率和 clean binary 误报率。
- 工具调用数量与无增益循环。
- 是否越权读取或执行。
- 成本、延迟和人工复核时间。

推荐候选：

- GPT-5.6 Sol。
- GPT-5.5 + Trusted Access。
- Grok 4.5。
- Gemini 3.1 Pro / 3.5 Flash。
- [Claude Opus 4.8](https://www.anthropic.com/news/claude-opus-4-8)、[Claude Sonnet 5](https://www.anthropic.com/news/claude-sonnet-5)；有资格时加入 [Mythos 5](https://www.anthropic.com/news/claude-fable-5-mythos-5)。
- Qwen3-Coder-Next 基础版与同底模 Heretic 版。

## AgentKey 与内置搜索的两轮产出对照

### 结论

在本次具体任务中，内置搜索重跑产出的来源更新，且一手来源比例更高。但这不是受控 A/B 实验：两轮查询数量、提示词、日期限制、站点限制、迭代次数、端点和预算均不同。它只能比较最终报告的召回结果，不能据此估计两种搜索方式固有的 precision、recall 或性价比。

| 维度 | AgentKey 上一版 | 内置搜索重跑 |
|---|---|---|
| 最新模型 | 停留在 Gemini 2.5、早期 Grok 讨论 | 命中 Grok 4.5、GPT-5.6、Gemini 3、Fable/Mythos 5 |
| 最新逆向论文 | 命中少量 2026 benchmark | 命中 2026-04 至 07 的完整新批次 |
| 官方 Cyber Access | 完全漏掉 | 命中 OpenAI TAC/GPT-5.5-Cyber、Anthropic Mythos 5 |
| GitHub 活跃度 | 以 README 摘要为主 | 可直接命中 release、弃用说明和近期仓库 |
| X/Twitter | 三次中两次零召回 | 能命中多条 2026 帖子，但噪声仍较高 |
| 原文核验 | Brave LLM Context 部分截断 | 可继续 open/find 到原文行 |
| 成本 | 估算 7.2 AgentKey credits | 未消耗 AgentKey credits；内置搜索的底层成本未按同一单位记录 |

### AgentKey 那次产出偏旧的可能原因

1. Brave `getLlmContext`可能更偏向适合作为 LLM 背景的高相关内容，经典论文和成熟页面因此可能获得较高排序。本轮没有使用同一查询对不同 provider 做重跑，尚不能确认其排序偏好。
2. AgentKey 查询没有强制 `2026`、近 30/90 天或发布日期排序。
3. 部分调用同时覆盖 GitHub、论文、模型和社区，搜索意图较宽。
4. Twitter 端点使用了较长的组合查询，两次零召回可能与查询结构、索引覆盖或端点排序有关，当前无法确定单一原因。
5. 上一版在出现“Grok 证据不足”后，没有用剩余额度对 `site:x.ai`、`site:docs.x.ai` 做精确补查。
6. 内置搜索本轮采用了明确站点限制、日期限制和发现后追查，因此查询设计本身更有利于发现新发布内容。

### 怎样公平地再次验证 AgentKey

下一次应采用完全相同的查询集和时间约束：

1. 每条查询只覆盖一个主题。
2. 强制包含 2026、过去 30/90 天或发布日期。
3. 分别查 `site:x.ai`、`site:openai.com`、`site:anthropic.com`、`site:arxiv.org`、`site:github.com`。
4. X 搜索拆成 Grok、Ghidra MCP、prompt injection 三条短查询。
5. 预先定义 20 个已知目标作为 recall set，例如 Grok 4.5、RARE、AutoDecompiler、TAC、Mythos 5。
6. 比较 Top-10 precision、新来源召回率、发布日期中位数、重复率、无结果率和每条有效来源成本。

只有这样才能区分是 AgentKey provider 能力不足，还是上一轮 query design 失误。

## 最终判断

截至 2026-07-16，建议优先验证的路线应调整为：

1. **官方 Trusted Cyber Access + 前沿模型 + 受控逆向工具链。** 当前优势是合规性、可审计性和较低误拒的设计目标，实际能力排名仍待内部 benchmark。
2. **强托管模型 + MCP/CLI agent + 确定性验证和工具授权。**
3. **本地 agentic coding 模型 + 领域微调或 Heretic 版本，用内部 benchmark 复测。**
4. **多模型路由、执行反馈、provenance 和信息流控制。**
5. **固定 JSON/System Prompt/prefill 越狱，仅作为红队研究对象。**

这份最新调研没有发现一个可以稳定解除 Grok 4.5、GPT-5.6、Fable 5 或 Gemini 3 全部限制的通用提示方法。厂商安全策略已经上移到模型训练、实时分类器、账户权限、身份验证、监控和产品沙箱。提示词最多突破其中某一层，而且会快速失效。

如果你的目标是真正构建 AI 逆向工作站，最值得做的下一步是建立一套本地 benchmark，然后让 Grok 4.5、GPT-5.6、Gemini 3.1、Claude 与本地 Heretic 模型在同一 Ghidra/radare2 工具层上跑。这个实验会比继续收集越狱 prompt 更接近真实答案。

## 调研限制

- 近 12 个月论文大多仍是预印本，作者自报数字需要独立复现。
- BinaryAudit 由单一团队维护，任务虽开放，但样本数量仍有限。
- Grok 4.5 发布仅一周，尚无专门逆向 benchmark。
- 厂商 benchmark 与 trusted-access 说明属于官方证据，存在产品叙事偏差。
- 搜索结果中的 X 帖子主要用于发现线索，不作为模型能力证明。
- 报告分析 jailbreak 机制与防御，但不保存可直接复用的绕过载荷。
