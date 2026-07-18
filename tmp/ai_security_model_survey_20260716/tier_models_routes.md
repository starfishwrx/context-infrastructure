# 证据线 A：开放权重“去对齐”模型与托管前沿模型的安全研究路线

检索日期：2026-07-16  
检索渠道：AgentKey（Brave `getLlmContext` 2 次；Sorsa `post_search_tweets` 1 次）  
范围：仅讨论授权逆向工程、恶意样本分析和防御性安全研究。本文不保存检索结果中出现的可复制越狱载荷、恶意代码、二进制绕过补丁或未授权攻击步骤。

## 结论先行

1. **“降低拒答”与“提升逆向工程能力”是两件事。** 开放权重模型可通过 refusal-direction abliteration、领域 SFT、偏好优化或模型合并显著降低拒答率，但公开证据多为模型作者自测。它们证明的是模型更愿意回答，不足以证明其反编译理解、漏洞判断或复杂工程综合能力超过原模型。
2. **开放权重路线的真实优势是控制权和隐私，而不只是“无道德限制”。** 本地部署允许研究者固定模型版本、审计提示与工具调用、隔离敏感样本、构造领域评测，并针对 Ghidra/IDA 输出做持续微调；代价是算力、上下文长度、工具集成和模型质量通常落后于顶级托管模型。
3. **托管前沿模型的有效路线是“agent + 工具 + 闭环验证”。** 将反编译器导出、调用图、运行时观测和测试结果交给 coding agent，比单纯依赖一段“解除限制”的 system prompt 更稳定。现有个案显示 Claude Code/Codex 能对长汇编文本进行结构分析，但单模型仍会误标循环层级、遗漏最优解释，因此必须交叉验证。
4. **没有高质量证据支持“Grok 或 Gemini 天生限制更低，所以更适合逆向工程”这一泛化。** 本轮针对 Grok/Gemini/Claude/Codex 的检索没有找到可复现的、同一安全任务集上的 Grok 对比基准。Gemini 的相关证据更多是通用 coding-agent 安全缺陷统计，并非逆向工程能力或拒答率测试。
5. **“无审查模型”会新增两类严重风险。** 第一，去除拒答方向可能损伤通用质量或事实可靠性；第二，反编译得到的字符串本身可能成为 prompt injection，诱导 agent 错判程序行为。安全工作流必须把反编译文本视为不可信数据，而不是指令。
6. **比寻找“最不受限模型”更可行的组合是双层架构：** 本地开放权重模型承担敏感材料预处理、批量标注和低风险静态分析；顶级托管模型只接收脱敏后的结构化证据，负责高难推理；最终结论由确定性工具、沙箱运行和第二模型复核。

## 一、开放权重与“去对齐”路线

### 1. Refusal-direction abliteration：直接修改权重中的拒答方向

Hugging Face 的 abliteration 教程说明，这类方法通过识别与拒答行为相关的激活方向，并对模型权重做正交化处理，使模型难以沿该方向产生拒答。教程同时明确承认：原模型在多个 benchmark 上显著优于 abliterated 版本，说明去除拒答会带来能力退化；后续 DPO 可以恢复大部分性能，但数学类任务仍可能未恢复。

- URL：https://huggingface.co/blog/mlabonne/abliteration
- 结果原文摘录：
  - “The ablation process successfully uncensored it but also degraded the model's quality.”
  - “This additional training allowed us to recover most of the performance drop ... One area where the model doesn't improve is GSM8K.”
- 来源层级：**一级方法资料 / 作者实验**。教程直接描述方法与作者评测，但不是独立同行复现。
- 适用判断：适合需要本地控制、可复现实验和拒答机制研究的团队；不能将“拒答减少”直接当作“安全分析更准确”。

### 2. 面向 coding 的 abliterated checkpoint：通用能力损失可能较小，也可能集中在特定维度

`huihui-ai/Qwen2.5-Coder-7B-Instruct-abliterated` 的模型卡给出了源模型与修改版对比：

- IF_Eval：63.14 → 61.90
- MMLU Pro：33.54 → 33.56
- TruthfulQA：51.804 → 48.8
- BBH：46.98 → 47.17
- GPQA：32.85 → 32.63

URL：https://huggingface.co/huihui-ai/Qwen2.5-Coder-7B-Instruct-abliterated

这些数据支持一个更细的判断：通用知识和推理 benchmark 可能变化不大，但 instruction following 和 truthfulness 会下降；对安全研究而言，后两者恰好非常关键。模型更少拒答，却可能更容易顺从错误前提或生成似是而非的解释。

- 来源层级：**一级模型卡 / 作者自报评测**。
- 冲突与局限：只包含通用 benchmark，没有反编译、漏洞定位、恶意样本分类或工具使用 benchmark。

### 3. 领域定向 abliteration：能更精确地降低网络安全类拒答，但证据仍主要来自作者

`Ornith-1.0-9B-uncensored-GGUF` 声称使用 400 个 offensive-security refusal probes 与 400 个 benign coding requests 提取网络安全领域拒答方向，结果由 31/100 拒答降至 4/100，且作者报告 KL divergence 0.0055。

- URL：https://huggingface.co/zaakirio/Ornith-1.0-9B-uncensored-GGUF
- 结果原文摘录：
  - “This release uses a cybersecurity-domain refusal direction.”
  - “Result: 31/100 → 4/100 offensive-security refusals (KL divergence 0.0055 — near-zero model quality loss).”
- 来源层级：**一级模型卡 / 作者自报领域评测**。
- 关键局限：拒答率和 KL divergence 不等于任务正确率；模型卡还用高风险任务“compliance”作卖点，不能视为安全性或专业性证明。

### 4. 自动化去拒答工具：降低人工调参门槛，但仍需独立 QA

GitHub 项目 `0xSojalSec/Uncensored-AI`（搜索结果将其描述为 Heretic）报告，在 Gemma 3 12B 上：

- 原模型：97/100 harmful prompts 拒答
- 两个公开 abliterated 版本：3/100 拒答，harmless prompts 上 KL divergence 分别为 1.04、0.45
- 项目作者版本：3/100 拒答，KL divergence 0.16

URL：https://github.com/0xSojalSec/Uncensored-AI

- 来源层级：**一级代码仓库 / 作者自报评测**。
- 能说明什么：自动化搜索或权重修改可以把拒答率压低，并在作者选定的分布上减少与源模型的偏差。
- 不能说明什么：没有证明其输出在逆向工程任务上更正确，也没有证明面对对抗性二进制、长调用图或模糊控制流时更可靠。

### 5. SFT、偏好优化与 personality conditioning：不是只有 abliteration 一条路

`Alxis955/qwe2.5-coder-Uncensored` 模型卡声称，逐阶段采用通用指令数据、对抗性请求数据和“uncensor/personality”数据后，基于 RefusalBench 的拒答率由基础模型的 53.04% 降至 5.89%。

- URL：https://huggingface.co/Alxis955/qwe2.5-coder-Uncensored
- 结果字段：53.04% → 49.82% → 10.89% → 5.89%
- 来源层级：**一级模型卡 / 作者自报评测**；模型卡关联一篇 2025 年 Applied Sciences 论文，但本轮未单独抓取、核验论文方法和结果。
- 局限：训练集本身包含高风险输出倾向，可能增加滥用能力；RefusalBench 只测“是否拒答”，不测技术正确性、隐蔽幻觉或防御用途。

### 开放权重路线的推荐使用方式

对授权研究，建议评价维度从“uncensored”改成五项：

1. **任务正确率**：函数识别、数据流恢复、协议字段推断、漏洞分类、PoC 解释是否可由专家或测试验证。
2. **拒答率**：在明确授权、隔离环境和防御目的下，是否仍对正常研究任务过度拒绝。
3. **幻觉率**：是否虚构符号、API、控制流或漏洞可利用性。
4. **工具闭环能力**：能否提出可验证假设，并调用反编译器、调试器、fuzzer 或测试脚本验证。
5. **数据边界**：能否完全离线运行，是否加载带 `trust_remote_code` 的不可信模型代码，模型及量化文件来源是否可审计。

## 二、Grok、Gemini、Claude、Codex 等托管模型的实际路线

### 1. 通过 coding agent 读取反编译器导出物

一篇 iOS 逆向工程实践文章比较 Claude Code 与 OpenAI Codex。作者将 Hopper 导出的汇编文本交给 agent 分析，报告两者都能理解复杂控制流，但各有错误：

- Claude 的优势：结构分析和标签更准确，首轮覆盖更完整，能提取更多 API/header 上下文。
- Codex 的优势：给出一个有效的更局部候选修改，但误标了循环层级，而且首轮并非最优。
- 作者的最终经验：“never trust a single agent’s output”；两个模型交叉验证后才发现各自遗漏。

URL：https://medium.com/@psychsecurity/automating-ios-reverse-engineering-with-ai-claude-code-vs-openai-codex-74491b5a38ae

- 来源层级：**二级实践个案 / 单作者经验**。
- 证据价值：说明“反编译器导出为文本 + filesystem-aware agent”是可工作的工程路线。
- 局限：不是受控 benchmark；文章包含对第三方应用保护机制的修改细节，本文不复述；没有 Grok 或 Gemini 同任务结果。

### 2. 通用 coding-agent 安全性不能从“能写代码”推断

Help Net Security 对一项 coding-agent 实验的报道中，研究者让 Claude Code（Sonnet 4.6）、Codex（GPT-5.2）和 Gemini（2.5 Pro）迭代开发应用：

- 30 个 PR 中 26 个至少包含一个漏洞，比例为 87%。
- 共发现 143 个安全问题。
- 最终扫描中，Claude、Gemini、Codex 的一个任务版本分别有 8、7、6 个问题；报道还称 Gemini 总体引入问题最多，并有最多高危发现。

URL：https://www.helpnetsecurity.com/2026/03/13/claude-code-openai-codex-google-gemini-ai-coding-agent-security/

- 原文摘录：“AI coding agents can produce working software at incredible speed, but security isn’t part of their default thinking.”
- 来源层级：**二级媒体报道 / 转述研究结果**。
- 局限：这是从零开发应用，不是逆向工程；不能据此给出模型能力总排名，但足以反驳“限制较少就更适合安全工作”的简单推论。

### 3. 本轮未找到 Grok 的可靠同场对比

Brave 检索没有返回 Grok 在反编译、接口逆向或恶意样本分析上的受控 benchmark。Twitter 结果中出现 Grok/Gemini 的多数内容是一般用户评价、情绪化比较或无关讨论，不足以支撑能力判断。

因此，对 Grok 的结论应保持为：

- 可将其作为候选 reasoning/API provider 接入 agent harness；
- 必须用同一套授权样本、同一工具权限和同一验收标准做内部评测；
- 不能把产品人格、“更敢回答”的主观印象或 X 平台上的零散体验当成专业安全能力证据。

## 三、Twitter/X 提供的两个重要新线索

### 1. 反编译文本 prompt injection 已成为逆向 agent 的专门攻击面

账号 `@0x0SojalSec` 转述美国 Naval Postgraduate School 研究，称攻击者可在正常二进制的字符串中嵌入指令；当 Ghidra/GhidraMCP/Cline 把反编译结果送给 Qwen3-8B agent 时，模型可能服从其中的提示，产生错误程序解释。

- 推文 URL：https://x.com/0x0SojalSec/status/2076413397802029464
- 结果字段：2026-07-12；840 likes；202 reposts；798 bookmarks；约 52,098 views。
- 原文摘录：“Instead of attacking the binary’s logic, attackers embed malicious prompt strings inside normal C code.”
- 来源层级：**三级社交媒体转述**。推文给出两篇论文标题，但本轮预算内未抓取论文原文，因此不能把具体实验结论视为已独立核验。
- 防御含义：
  - 将反编译字符串、注释、资源文本和符号名标记为不可信数据；
  - system prompt 明确禁止将样本内容解释为控制指令；
  - 工具层对来自样本的文本做 provenance 标注；
  - 关键结论由控制流、动态执行和第二模型独立复核。

这条证据直接削弱了“只要模型不拒答，就能更好做逆向”的思路：模型越顺从，反而可能越容易被目标样本中的提示劫持。

### 2. 闭环观测比单轮生成更重要

账号 `@MiguelNeves` 描述一个硬件逆向案例：agent 通过摄像头观察设备对命令的响应，把结果反馈到调查中，形成 observe-test-learn-iterate 的闭环。

- 推文 URL：https://x.com/MiguelNeves/status/2077466379322605659
- 结果字段：2026-07-15；作者为 verified；约 84 views，互动很少。
- 原文摘录：“it turns hardware reverse engineering into a closed loop.”
- 来源层级：**三级个案陈述 / 未独立验证**。
- 证据价值：不是模型性能证明，但指向正确的系统设计——把模型当作提出假设和安排实验的 agent，而不是最终事实来源。

### 3. 托管 coding agent 的代码外传风险需要单独审计

账号 `@IntCyberDigest` 声称，xAI 的 Grok Build CLI 在 beta 期间曾把完整 Git 仓库上传到云存储，并在后续关闭默认 retention、删除已保留 coding data、准备开源 CLI。该帖称信息来自网络流量观察和厂商声明，但本轮没有抓取 xAI 原始公告或独立技术报告。

- 推文 URL：https://x.com/IntCyberDigest/status/2077502378375324135
- 结果字段：2026-07-15；775 likes；96 reposts；186 bookmarks；约 77,962 views。
- 来源层级：**三级媒体账号转述 / 未核验指控**。
- 使用限制：不能作为“已确认 xAI 泄露用户仓库”的事实引用；可以作为采购和上线前必须验证的风险假设。
- 最小审计项：抓包确认上传范围、检查 ZDR/retention 合同、使用隔离测试仓库、禁止 agent 默认读取整个 monorepo、对 secrets 做预扫描。

## 四、路线比较

| 路线 | 主要收益 | 主要缺陷 | 当前证据强度 | 适合场景 |
|---|---|---|---|---|
| 本地原始开放权重 coding model | 隐私、版本固定、可审计 | 仍可能过度拒答；能力受模型规模限制 | 中 | 敏感样本静态分析、批量分类 |
| Abliterated / uncensored checkpoint | 显著降低拒答，可完全离线 | 可能损伤 instruction following、truthfulness；作者自测多 | 中低 | 拒答机制研究、受控红队评测 |
| 领域 SFT / DPO / LoRA | 可针对反编译术语、工具轨迹和报告格式优化 | 数据污染、灾难性遗忘、双用途能力提升 | 中低 | 有内部高质量数据和评测团队 |
| 托管前沿模型 + coding agent | 长上下文、强推理、成熟工具调用 | 服务端策略仍在；数据和 retention 风险 | 中 | 脱敏后的复杂控制流与多文件推理 |
| 多模型交叉验证 | 暴露单模型的结构误判和遗漏 | 成本、延迟、错误可能相关 | 中 | 高价值结论、发布前复核 |
| 反编译器/调试器闭环 agent | 结论可被工具和实验验证 | 工具权限与 prompt injection 面扩大 | 中 | 授权实验室、硬件/协议逆向 |
| 单纯 system prompt / JSON 前缀“解除限制” | 成本低、易试验 | 脆弱、版本相关、不可审计，且不能提升基础能力 | 低 | 仅适合内部鲁棒性测试，不应作为生产路线 |

## 五、冲突、空白与研究局限

1. **自报 benchmark 偏差。** Hugging Face 模型卡与 GitHub README 是最接近实现的一手资料，但作者同时是模型发布者；拒答数据需要独立复测。
2. **测量目标错位。** 几乎所有 uncensored 项目优化的是 refusal rate 或 harmless-distribution KL，而用户真正需要的是逆向任务的正确率、证据可追溯性和幻觉率。
3. **托管模型版本漂移。** Claude、Codex、Gemini、Grok 的服务端模型、安全策略和工具权限会变化；一次个案不能长期代表产品。
4. **Grok 证据不足。** 本轮没有找到 Grok 与其他模型在授权逆向工程任务上的可复现对比，不能支持“Grok 限制更低且更有效”的结论。
5. **Twitter 只能发现线索。** 反编译 prompt injection、硬件闭环和 Grok Build 数据上传均需回到论文、代码或厂商公告核验。
6. **搜索结果含潜在危险文本。** 个别模型卡返回了直接恶意任务示例和可运行代码；本报告已主动省略，不将其作为模型质量证据。

## 六、给总报告的建议

最终报告不宜以“如何去除道德限制”为主轴，而应改为：

> 如何为授权安全研究构建低误拒、可审计、抗提示注入、能用工具验证的 AI 逆向工程工作流。

推荐的验证架构：

1. 本地模型先解析敏感样本，输出结构化中间表示与 provenance。
2. 对托管模型只提供最小必要、已脱敏的函数片段、调用图和运行结果。
3. system prompt 只定义授权范围、数据/指令边界和证据格式，不依赖“角色扮演解锁”。
4. 第一模型提出假设；确定性工具或沙箱实验验证；第二模型在看不到第一模型推理的条件下独立复核。
5. 评分以正确率、可验证性、幻觉率、prompt-injection resistance 和数据边界为主，拒答率只是一个次级指标。

## AgentKey 调用记录

- 成功付费调用：3 次
  - Brave/getLlmContext：2 次 × 0.6 credits
  - Sorsa/post_search_tweets：1 次 × 1.0 credit
  - 合计：2.2 credits
- 额外验证失败：1 次。第一次 Brave 调用误用了 `query` 字段，服务返回 `missing required param: q`；按工具建议改为 `q` 后重试成功。该次没有返回搜索数据，通常不应计为成功付费调用，但最终账单应以 AgentKey 账户记录为准。
- 未使用内置 Web Search/WebFetch；未追加检索预算。
