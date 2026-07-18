# 证据线 B：System Prompt 前缀、结构化注入与对齐绕过

> 范围：机制、跨模型可靠性、供应商修补与失败边界。本文不保存或复述可直接复制的越狱载荷、对抗后缀、角色伪造模板或审核规避步骤。

## 执行记录

- AgentKey 付费调用：**3 次**
  - `Brave/getLlmContext`：2 次 × 0.6 credit
  - `Sorsa/post_search_tweets`：1 次 × 1 credit
- 实际消耗：**2.2 credits**
- 免费发现/校验调用：`tools/list` 1 次，`describe_tool` 2 次。
- X/Twitter 查询返回：**0 条推文**。因此本文件没有把任何网页或 GitHub 内容冒充 X 证据，也没有超预算重试。

## 先给结论

1. **“在 System Prompt 开头塞一段 JSON/XML 就能解除道德限制”不是稳定技术。**  
   JSON、XML、Markdown、代码块等格式本身没有更高权限。它们至多改变模型对文本的语义分组、角色判断和续写先验。若结构化文本仍处于 user message，其权限通常仍低于真实 system/developer message；效果高度依赖模型、chat template、API 是否支持 assistant prefill，以及供应商当时的安全补丁。

2. **更有实证基础的机制不是“JSON 魔法”，而是角色混淆、上下文续写和控制面/数据面混合。**  
   当应用把系统指令、用户输入、网页/RAG 内容、工具返回拼进同一个 token 流时，模型只能以学习到的统计模式区分“指令”和“数据”。伪角色标记、虚构对话历史、assistant prefill、长上下文逐步诱导，都是在操纵这种 learned representation，而不是获得真正的系统权限。

3. **可迁移攻击存在，但“通用”不等于长期可靠。**  
   GCG、AmpleGCG、PRP 等研究说明某些对抗模式能从开源模型迁移到闭源模型；PAIR、TAP、adaptive random search 等黑盒方法则通过迭代适应目标模型。但成功率会随着模型版本、chat template、输入规范化、独立 moderation/classifier 和供应商补丁迅速变化。

4. **静态前缀最容易被修补；自适应、多轮和 agent/RAG 场景更难防。**  
   固定字符串或固定 JSON schema 很容易进入训练集、黑名单或模板清洗规则。相对而言，自适应搜索、多轮上下文塑形、间接 prompt injection 和工具输出中的角色混淆更能绕开只检查单轮输入的防线，但代价是查询数、成本、不确定性和可检测性上升。

5. **对安全研究工作流而言，可靠路线是授权模型与隔离架构，不是押注某个越狱前缀。**  
   如果目标是接口逆向、反编译和漏洞分析，应优先使用本地权重模型、明确允许安全研究的 API/模型、最小权限工具、沙箱和人工审批。Prompt bypass 最适合作为红队评估对象，而不是生产能力的稳定依赖。

## 关键概念：不要把三类问题混在一起

| 类别 | 攻击目标 | 典型机制 | 与 JSON/XML 的关系 |
|---|---|---|---|
| Jailbreak | 让模型违反其内容安全策略 | 对抗后缀、角色扮演、说服、多轮渐进、自适应搜索 | 结构化格式只是包装或语义伪装，不提供真实权限 |
| Direct prompt injection | 让应用内的模型忽略开发者任务，执行用户冲突指令 | 指令优先级混淆、上下文覆盖 | JSON/XML 可能让冲突指令看起来像配置或高权威元数据 |
| Indirect prompt injection | 恶意指令藏在网页、文档、代码、issue、工具输出中 | 控制面与不可信数据面混合；agent 读取后误执行 | 结构化内容可伪装为工具协议、对话历史或系统字段，agent 场景风险更高 |

## 学术证据与项目

### 1. JailbreakBench：先解决“成功率不可比”

- 论文：[JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models](https://arxiv.org/abs/2404.01318)
- 代码：[JailbreakBench/jailbreakbench](https://github.com/JailbreakBench/jailbreakbench)
- Leaderboard：[jailbreakbench.github.io](https://jailbreakbench.github.io/)
- 会议版本：[NeurIPS 2024 paper](https://proceedings.neurips.cc/paper_files/paper/2024/file/63092d79154adebd7305dfd498cbff70-Paper-Datasets_and_Benchmarks_Track.pdf)

返回摘录：

> “there is no clear standard of practice regarding jailbreaking evaluation”

> “numerous works are not reproducible”

可靠性判断：**高**。NeurIPS Datasets and Benchmarks 论文、开放代码和 leaderboard，适合作为方法比较的基线。它同时提醒：闭源 API 持续变化、攻击成本口径不同、judge 不一致，会使网上流传的“成功率”缺乏可比性。

对本问题的意义：任何声称“某段 JSON 对所有模型都有效”的说法，如果没有固定模型版本、system prompt、chat template、judge、行为集和查询预算，不能视为可复现实证。

### 2. Universal and transferable attacks：证明“跨模型迁移”存在，但不是永久钥匙

- 论文：[Universal and Transferable Adversarial Attacks on Aligned Language Models](https://arxiv.org/abs/2307.15043)
- 相关生成式路线：[AmpleGCG](https://arxiv.org/abs/2404.07921)
- 相关传播路线：[PRP](https://arxiv.org/abs/2402.15911)
- 论文/代码索引：[JailbreakZoo](https://github.com/Allen-piexl/JailbreakZoo/blob/main/Papers/LLM_Jailbreak.md)

AgentKey 返回的论文索引将 GCG描述为优化“universal/transferable adversarial suffix”，并列出 AmpleGCG、PRP 等后续路线。

可靠性判断：**中高**。跨模型迁移是经过论文验证的真实现象，但外推到最新闭源模型时必须谨慎：

- 优化通常依赖源模型梯度或代理模型；
- tokenizer、chat template、系统提示和解码参数变化会破坏迁移；
- 闭源模型还可能有输入/输出 classifier 与服务器端策略；
- 公开后缀容易被定向训练和规则过滤；
- “对若干模型迁移成功”不等于“对任意新模型长期有效”。

### 3. 自适应黑盒攻击：供应商修补后的主要压力测试

- 论文：[Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks](https://openreview.net/pdf?id=A6NDhcjXvC)
- 代码：[tml-epfl/llm-adaptive-attacks](https://github.com/tml-epfl/llm-adaptive-attacks)
- 相关方法索引：[Awesome-Jailbreak-on-LLMs](https://github.com/yueliu1999/Awesome-Jailbreak-on-LLMs)

返回摘录：

> “provide the code, prompts, and logs of the attacks”

可靠性判断：**高于静态社区 prompt，低于固定版本白盒实验的可重复性**。其强项是针对目标模型即时调整，弱点是：

- 成功依赖查询预算和 attacker/judge 模型；
- API 漂移会改变结果；
- 供应商可能根据异常重复查询、语义聚类或输出审查拦截；
- 实验中的高 ASR 不等于真实 agent 能完成后续工具调用。

### 4. StruQ：结构化查询是防御思路，不是“JSON 解锁”

- 论文：[StruQ: Defending Against Prompt Injection with Structured Queries](https://arxiv.org/html/2402.06363v2)

返回摘录：

> “a single string that mixes control (the prompt) with data”

StruQ 的核心判断是，传统 LLM API 把控制指令与不可信数据混在一个字符串里，属于 unsafe-by-design。其方案是把指令/数据通道结构化分离，并用模拟 injection 的训练强化这种边界。

可靠性判断：**高**。这是理解 JSON/XML 现象的关键反证：如果仅在同一个 user string 里加标签，仍没有真正的权限隔离。有效的“结构化”需要应用协议、模型训练或受控解析器共同支持，而不是只换一种文本外观。

### 5. Chat template / role-token confusion：结构化前缀最可信的机制解释

- 论文：[ChatInject: Abusing Chat Templates for Prompt Injection in LLM Agents](https://arxiv.org/html/2509.22830v2)
- OpenReview 版本：[ChatInject PDF](https://openreview.net/pdf?id=WVhgFSKniL)

返回摘录：

> “it misinterprets the subsequent content as originating from a higher-priority role”

> “exploits LLM chat templates to perform effective indirect prompt injection”

论文把攻击面定位在模型学习到的 chat template 和角色分段标记：如果不可信工具输出中出现模型熟悉的结构标记，模型可能把数据误识别为更高优先级对话内容。

可靠性判断：**中高，但需关注发布日期与复现范围**。它比“JSON 解除限制”的解释更具体，也更贴近 agent/RAG 系统。边界包括：

- 必须知道或猜中目标模型的模板模式；
- API/SDK 可能转义、剥离或重新编码特殊标记；
- 不同模型的角色 token 不同；
- 服务器端不会因为文本长得像 system message，就真的把它放入 system channel；
- 格式清洗可以降低效果，但论文也指出轻微变形可能削弱纯规则清洗。

### 6. Instruction hierarchy：供应商试图把权限顺序训练进模型

- 论文：[The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions](https://arxiv.org/abs/2404.13208)

AgentKey 返回的防御汇总将其描述为训练模型遵守 system > user > tool/content 的优先级，并指出它是 learned prior，而不是硬安全边界。

可靠性判断：**中高**。方向合理且是供应商修补的核心路线，但仍属于概率性模型行为。它能显著降低直接覆盖类攻击，却不能替代工具权限控制、数据来源标记和输出审批。

### 7. Spotlighting：分隔符有帮助，但不是强隔离

- 论文：[Defending Against Indirect Prompt Injection Attacks With Spotlighting](https://arxiv.org/abs/2403.14720)

检索结果概括其通过 delimiter、datamarking 或编码标记不可信文本，让模型更容易区分数据与指令。

可靠性判断：**中高**。它支持“结构化标记会影响模型判断”，但方向是降低 injection，而不是自动提高攻击权限。局限是：

- 仍然依赖模型正确理解标记；
- 可能损害长文本和代码理解；
- 对新型语义、多轮、混淆或多模态攻击的覆盖有限；
- 若 agent 给不可信内容真实工具权限，单靠标记不能提供安全保证。

### 8. 结构性隔离：CaMeL 比 prompt hardening 更接近安全边界

- 论文：[CaMeL: Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813)

AgentKey 返回的防御汇总描述其将 privileged planner 与处理不可信数据的 quarantined model 分开，并通过解释器跟踪 provenance 和执行 policy。

可靠性判断：**中高**。这是更接近工程安全的方向：即便模型被诱导，也没有无限制工具权限。代价是策略编写、系统复杂度、用户审批和任务效用损失。

## JSON/XML、System Prompt 前缀与 assistant prefill：逐项判断

### JSON/XML 包装

**机制级解释**

- 训练语料中，JSON/XML 常与配置、协议、工具调用、元数据和高权威文档同时出现，可能改变模型对内容的先验判断。
- 明确字段名和层级可帮助模型把某些文本视为“规则”而非普通对话。
- 反过来，供应商也用 XML/delimiter 标记不可信数据；所以格式本身并不天然偏向攻击者或防御者。

**可靠性：低到中**

- 对特定模型、特定模板、特定时间点可能有效；
- 跨模型迁移弱于模型专属自适应攻击；
- JSON 语法正确与否通常不是决定因素，模型理解的是 token 模式而非真正执行 schema；
- 仅作为 user content 时无法获得真实 system-channel 权限。

**常见失效**

- 模型明确遵循 instruction hierarchy；
- SDK 把整个 JSON 作为普通 user content；
- 输入规范化或 tool schema validation 删除未知字段；
- 独立安全 classifier 根据语义而非格式判断；
- 供应商对流行模板做 adversarial training。

### “System Prompt 头几句注入”

需要区分两种情况：

1. **开发者真正控制 system/developer message**：这是正常配置，不是越狱。它能放宽应用层指令，但不能保证关闭模型权重层对齐、服务器端 moderation 或供应商政策。
2. **用户把一段文本伪装成 system prompt**：这仍是低权限文本，只可能诱发角色混淆；是否有效取决于模型训练和应用拼接方式。

**可靠性：**

- 真 system channel：能稳定改变任务行为，但不能承诺去掉全部安全层；
- 伪 system 文本：低到中，且容易被 instruction hierarchy、模板转义和输入清洗修补。

### Assistant prefill

**机制级解释**

如果 API 允许开发者预置 assistant response 的开头，模型会倾向于延续已经开始的语义和格式。它利用的是自回归续写惯性与“保持角色一致”的训练先验。

**可靠性：中，但强依赖接口**

- 只在允许 assistant prefill 或可控历史消息的接口中存在；
- 普通聊天 UI 往往不暴露该能力；
- 新 API 可能禁止末条 assistant message、重写历史或执行安全扫描；
- 服务器端 output classifier 仍可拦截最终结果；
- 对模型版本和具体拒绝策略高度敏感。

因此 prefill 是一个真实攻击面，但不能概括为“任意 JSON 前缀即可解锁”。

## 跨模型可靠性矩阵

| 方法族 | 初始成功潜力 | 跨模型迁移 | 对供应商补丁耐受 | 主要失败边界 |
|---|---:|---:|---:|---|
| 固定角色扮演/固定前缀 | 中 | 低 | 很低 | 黑名单、训练覆盖、instruction hierarchy |
| JSON/XML/代码样式包装 | 低-中 | 低-中 | 低 | 仍属 user channel；语义 classifier 不看外观 |
| Assistant prefill | 中-高 | 中 | 低-中 | API 不支持；历史重写；输出审查 |
| 特殊 token/chat-template 混淆 | 高（条件满足时） | 中 | 中 | 模板差异、转义、格式剥离、角色 token 更新 |
| 通用对抗后缀 | 高（论文固定环境） | 中 | 低 | tokenizer/template/版本变化；定向过滤 |
| 黑盒自适应搜索 | 高 | 中-高 | 中-高 | 查询成本、速率限制、检测、模型漂移 |
| 多轮渐进/上下文塑形 | 中-高 | 中-高 | 中 | conversation-level classifier、上下文摘要/重置 |
| 间接 prompt injection in agents | 高影响 | 中 | 中-高 | provenance、数据/控制分离、最小权限、审批 |

## 供应商修补如何改变结论

### 常见修补层

1. **模型训练层**：instruction hierarchy、adversarial training、RLAIF/RLHF、拒绝泛化。
2. **输入层**：模板规范化、特殊 token 转义、prompt classifier、已知模式过滤。
3. **推理层**：安全感知 decoding、上下文风险评分、异常多轮检测。
4. **输出层**：独立 moderation/classifier、敏感内容复核。
5. **Agent 架构层**：工具最小权限、来源标记、taint/provenance、审批、隔离执行。

### 为什么“昨天可用的 prompt”今天会失效

- 闭源模型和系统提示会静默更新；
- 公开传播的 payload 会进入红队集和训练数据；
- chat template 或 tokenizer 变化会破坏 token 级攻击；
- 产品层可能新增 classifier，而基础模型本身没有变化；
- 供应商可对高频攻击模式做精确封堵；
- benchmark judge 与真实产品 policy 不一致。

## 防御与失败案例

### Prompt hardening / sandwich defense

用途：给模型更清晰的边界，用 XML/delimiter 包围不可信文本。

失败原因：它仍是自然语言约束，不是访问控制。复杂语义、多轮诱导、模板伪造和间接 injection 可能让模型重新解释边界。

### Perplexity / 字符级过滤

用途：识别低流畅度对抗后缀。

失败原因：可读的语义攻击、说服型攻击、自适应黑盒攻击不一定表现为高 perplexity。

### 输入/输出 classifier

用途：把安全判断从主模型中分离。

失败原因：新型语义、上下文分散、编码和多轮攻击可降低召回；classifier 自身也可能存在对抗脆弱性；过强会造成 over-refusal。

### 格式剥离与特殊 token 转义

用途：针对 chat-template/role-token confusion。

失败原因：纯规则解析对轻微变形、模型隐式恢复角色结构、不同模态或新模板覆盖不足。更稳妥的做法是把不可信数据置于无工具权限的隔离处理链。

### Adversarial training

用途：补齐已知攻击分布。

失败原因：对 OOD、长上下文、新模型生成的自适应攻击和新模态泛化有限；还可能增加正常请求拒绝率。

## X/Twitter 结果

查询覆盖：JSON、XML、assistant prefill、system prompt、jailbreak、prompt injection、model safety、bypass，排序为 popular，并排除 replies。

结果：**0 条**。

可得结论仅限于：本轮 Sorsa 查询没有提供可引用的 X 社区证据。不能据此推断 X 上不存在相关讨论；也不能为了填补空缺而把 GitHub gist 或安全博客当作推文证据。

## 对主报告的建议表述

建议写成：

> JSON/XML 前缀、伪 system 字段和 assistant prefill 并不是“删除模型道德限制”的统一开关。它们利用的是模型对角色、格式和续写上下文的统计性判断；在特定模型与接口上可能短期有效，但对版本、chat template、产品层审核和供应商补丁高度敏感。学术上更稳固的结论是：LLM 应用把控制指令与不可信数据混在同一 token 流，造成角色混淆和 prompt injection；工程上应以结构化通道、权限隔离、provenance 和独立审核解决，而不是依赖更强的提示词。

不建议写成：

> 在 system prompt 开头放某个 JSON 就能稳定解除 Grok/Gemini 的安全限制。

原因：现有证据不支持跨模型、跨版本和长期稳定性；而且这会把模型行为诱导错误描述成真实权限提升。

## 来源索引

### 一手论文、基准与代码

- [JailbreakBench paper](https://arxiv.org/abs/2404.01318)
- [JailbreakBench GitHub](https://github.com/JailbreakBench/jailbreakbench)
- [JailbreakBench leaderboard](https://jailbreakbench.github.io/)
- [Universal and Transferable Adversarial Attacks](https://arxiv.org/abs/2307.15043)
- [AmpleGCG](https://arxiv.org/abs/2404.07921)
- [PRP](https://arxiv.org/abs/2402.15911)
- [Adaptive attacks paper](https://openreview.net/pdf?id=A6NDhcjXvC)
- [Adaptive attacks code](https://github.com/tml-epfl/llm-adaptive-attacks)
- [StruQ](https://arxiv.org/html/2402.06363v2)
- [Instruction Hierarchy](https://arxiv.org/abs/2404.13208)
- [Spotlighting](https://arxiv.org/abs/2403.14720)
- [ChatInject](https://arxiv.org/html/2509.22830v2)
- [CaMeL](https://arxiv.org/abs/2503.18813)

### 聚合索引，仅用于发现，不作为单独验证

- [JailbreakZoo](https://github.com/Allen-piexl/JailbreakZoo/blob/main/Papers/LLM_Jailbreak.md)
- [Awesome-Jailbreak-on-LLMs](https://github.com/yueliu1999/Awesome-Jailbreak-on-LLMs)
- [JailTrickBench](https://github.com/usail-hkust/JailTrickBench)
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

## 证据限制

- Brave 返回内容在终端中发生截断；本文件只使用了可见结果中的 URL 和短摘录。
- 第二次检索包含 2025-2026 的新论文，其中部分尚需更多独立复现；已降低其可靠性评级。
- X 检索为空，因此社区流行度与实际操作反馈本轮未得到验证。
- 未对任何闭源模型执行 jailbreak，也未验证具体 payload；本文结论是机制与公开证据层面的判断。
